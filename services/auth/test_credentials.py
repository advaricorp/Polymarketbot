#!/usr/bin/env python3
"""
Test script to verify Polymarket API credentials and fetch basic market data.
"""

import os
import logging
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from py_clob_client.exceptions import PolyApiException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_credentials():
    """Test the API credentials and fetch some basic market data."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get credentials from environment
        api_key = os.getenv("POLY_API_KEY")
        api_secret = os.getenv("POLY_API_SECRET")
        passphrase = os.getenv("POLY_PASSPHRASE")
        private_key = os.getenv("POLY_PRIVATE_KEY")
        
        # Debug log environment variables
        logger.info("Environment variables:")
        logger.info(f"POLY_API_KEY: {'*' * len(api_key) if api_key else 'None'}")
        logger.info(f"POLY_API_SECRET: {'*' * len(api_secret) if api_secret else 'None'}")
        logger.info(f"POLY_PASSPHRASE: {'*' * len(passphrase) if passphrase else 'None'}")
        logger.info(f"POLY_PRIVATE_KEY: {'*' * len(private_key) if private_key else 'None'}")
        
        if not all([api_key, api_secret, passphrase, private_key]):
            raise ValueError("Missing required environment variables")
            
        # Add 0x prefix to private key if missing
        if not private_key.startswith("0x"):
            private_key = "0x" + private_key
        
        # Initialize API credentials
        creds = ApiCreds(
            api_key=api_key,
            api_secret=api_secret,
            api_passphrase=passphrase
        )
        
        # Initialize CLOB client
        logger.info("Initializing CLOB client...")
        client = ClobClient(
            host="https://clob.polymarket.com",
            key=private_key,
            chain_id=137,
            creds=creds
        )
        
        # Test 1: Get wallet address
        address = client.get_address()
        logger.info(f"✅ Connected with address: {address}")
        
        # Test 2: Verify API keys
        logger.info("Verifying API keys...")
        api_keys = client.get_api_keys()
        logger.info("✅ API keys verified")
        
        # Test 3: Get some active markets
        logger.info("Fetching active markets...")
        markets = client.get_markets()
        total_markets = len(markets.get('data', []))
        logger.info(f"✅ Found {total_markets} active markets")
        
        # Test 4: Get order book for an active market
        if markets.get('data'):
            # Try to find a market with active trading
            for market in markets['data']:
                if not market.get('active') or market.get('closed'):
                    continue
                    
                tokens = market.get('tokens', [])
                if not tokens:
                    continue
                    
                token_id = tokens[0].get('token_id')
                question = market.get('question', 'Unknown')
                
                try:
                    logger.info(f"Fetching order book for market: {question}")
                    book = client.get_order_book(token_id)
                    
                    # Check if there's actual liquidity
                    if book.get('bids') or book.get('asks'):
                        logger.info("✅ Successfully fetched order book with liquidity:")
                        logger.info(f"  Market: {question}")
                        logger.info(f"  - Best bid: {book['bids'][0]['price'] if book.get('bids') else 'No bids'}")
                        logger.info(f"  - Best ask: {book['asks'][0]['price'] if book.get('asks') else 'No asks'}")
                        break
                    else:
                        logger.info("No liquidity in this market, trying next...")
                        continue
                        
                except PolyApiException as e:
                    logger.info(f"No order book for market {question}: {str(e)}")
                    continue
                    
        logger.info("\n🎉 All tests passed! API credentials are working correctly.")
        logger.info("\nSummary:")
        logger.info(f"✓ Connected to address: {address}")
        logger.info(f"✓ API Key verified: {api_key}")
        logger.info(f"✓ Found {total_markets} active markets")
        logger.info("\nYou can now start using these credentials in your bot!")
        
    except ValueError as e:
        logger.error(f"❌ Error testing credentials: {str(e)}")
        raise
    except PolyApiException as e:
        logger.error(f"❌ Error testing credentials: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        raise

if __name__ == "__main__":
    test_credentials() 