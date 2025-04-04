"""
Tests for the market data ingestion service.
"""

import os
import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds

from services.ingest.market_data import MarketState, MarketDataService

# Load test environment
load_dotenv()

@pytest.fixture
def mock_client():
    """Create a mock Polymarket client."""
    client = Mock(spec=ClobClient)
    # Add async methods that we'll use
    client.get_markets = AsyncMock()
    client.get_order_book = AsyncMock()
    return client

@pytest.fixture
def market_data():
    """Sample market data for testing."""
    return {
        'data': [
            {
                'condition_id': 'market1',
                'question': 'Will X happen?',
                'tokens': [
                    {'token_id': 'yes1', 'outcome': 'YES'},
                    {'token_id': 'no1', 'outcome': 'NO'}
                ],
                'active': True,
                'closed': False
            },
            {
                'condition_id': 'market2',
                'question': 'Will Y happen?',
                'tokens': [
                    {'token_id': 'yes2', 'outcome': 'YES'},
                    {'token_id': 'no2', 'outcome': 'NO'}
                ],
                'active': True,
                'closed': False
            }
        ]
    }

@pytest.fixture
def order_book_data():
    """Sample order book data for testing."""
    return {
        'bids': [{'price': '0.60', 'size': '100.0'}],
        'asks': [{'price': '0.65', 'size': '100.0'}]
    }

@pytest.mark.asyncio
async def test_market_state_calculations():
    """Test MarketState property calculations."""
    state = MarketState(
        condition_id='test',
        question='Test market?',
        token_ids=['yes', 'no'],
        best_bid=0.60,
        best_ask=0.65
    )
    
    assert state.spread == 0.05
    assert state.midpoint == 0.625

@pytest.mark.asyncio
async def test_service_initialization(mock_client):
    """Test MarketDataService initialization."""
    service = MarketDataService(mock_client)
    assert service.client == mock_client
    assert service.update_interval == 1.0
    assert service.max_markets == 100
    assert not service._running
    assert len(service._markets) == 0

@pytest.mark.asyncio
async def test_service_start_stop(mock_client):
    """Test starting and stopping the service."""
    service = MarketDataService(mock_client)
    
    # Start service
    await service.start()
    assert service._running
    assert len(service._tasks) == 1
    
    # Stop service
    await service.stop()
    assert not service._running
    assert len(service._tasks) == 0

@pytest.mark.asyncio
async def test_callback_registration(mock_client):
    """Test callback registration and notification."""
    service = MarketDataService(mock_client)
    
    # Create a mock callback
    callback = Mock()
    service.add_callback(callback)
    assert len(service._callbacks) == 1
    assert service._callbacks[0] == callback

@pytest.mark.asyncio
async def test_market_updates(mock_client, market_data, order_book_data):
    """Test market data updates."""
    service = MarketDataService(mock_client, update_interval=0.1)
    
    # Setup mock responses
    mock_client.get_markets.return_value = market_data
    mock_client.get_order_book.return_value = order_book_data
    
    # Start service
    await service.start()
    
    # Let it run for a bit
    await asyncio.sleep(0.2)
    
    # Stop service
    await service.stop()
    
    # Verify market data was fetched
    mock_client.get_markets.assert_called()
    
    # TODO: Add more assertions once _fetch_markets and _update_markets are implemented

@pytest.mark.asyncio
async def test_error_handling(mock_client):
    """Test error handling in update loop."""
    service = MarketDataService(mock_client, update_interval=0.1)
    
    # Setup mock to raise an exception
    mock_client.get_markets.side_effect = Exception("Test error")
    
    # Start service
    await service.start()
    
    # Let it run for a bit
    await asyncio.sleep(0.2)
    
    # Stop service
    await service.stop()
    
    # Verify service continued running despite errors
    assert mock_client.get_markets.call_count > 1

@pytest.mark.asyncio
async def test_market_state_retrieval(mock_client, market_data):
    """Test getting market states."""
    service = MarketDataService(mock_client)
    
    # Manually add some market states
    state = MarketState(
        condition_id='test',
        question='Test market?',
        token_ids=['yes', 'no']
    )
    service._markets['test'] = state
    
    # Test retrieval
    assert service.get_market_state('test') == state
    assert service.get_market_state('nonexistent') is None
    assert len(service.get_all_markets()) == 1

@pytest.mark.integration
@pytest.mark.skipif(not os.getenv('RUN_INTEGRATION_TESTS'), reason="Integration tests not enabled")
async def test_integration_with_real_client():
    """Integration test with real Polymarket client.
    
    Note: This test is skipped by default. To run it:
    1. Set RUN_INTEGRATION_TESTS=1 in your environment
    2. Ensure you have valid Polymarket API credentials in your .env file
    """
    # Load credentials from .env
    api_key = os.getenv("POLY_API_KEY")
    api_secret = os.getenv("POLY_API_SECRET")
    passphrase = os.getenv("POLY_PASSPHRASE")
    private_key = os.getenv("POLY_PRIVATE_KEY")
    
    if not all([api_key, api_secret, passphrase, private_key]):
        pytest.skip("Missing required environment variables for integration test")
    
    # Add 0x prefix to private key if missing
    if not private_key.startswith("0x"):
        private_key = "0x" + private_key
    
    # Create real client
    creds = ApiCreds(
        api_key=api_key,
        api_secret=api_secret,
        api_passphrase=passphrase
    )
    
    client = ClobClient(
        host="https://clob.polymarket.com",
        key=private_key,
        chain_id=137,
        creds=creds
    )
    
    # Create service
    service = MarketDataService(client, update_interval=1.0)
    
    # Start service
    await service.start()
    
    # Let it run for a few seconds
    await asyncio.sleep(3)
    
    # Stop service
    await service.stop()
    
    # Verify we got some market data
    markets = service.get_all_markets()
    assert len(markets) > 0  # Should have found some markets 