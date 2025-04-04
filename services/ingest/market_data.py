"""
Market Data Ingestion Service

This service is responsible for:
1. Maintaining WebSocket connections to Polymarket
2. Processing real-time market data updates
3. Managing market state and order book updates
4. Providing clean interfaces for other services to access market data
"""

import logging
import asyncio
import json
from typing import Dict, List, Optional, Callable, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, RequestArgs
from py_clob_client.endpoints import GET_MARKETS, GET_ORDER_BOOK
from py_clob_client.http_helpers.helpers import get
from py_clob_client.headers.headers import create_level_2_headers

logger = logging.getLogger(__name__)

@dataclass
class MarketState:
    """Represents the current state of a market."""
    market_id: str
    condition_id: str
    token_ids: List[str]
    best_bid_price: Optional[float] = None
    best_ask_price: Optional[float] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    last_update: datetime = field(default_factory=datetime.now)
    
    @property
    def spread(self) -> Optional[float]:
        """Calculate the current spread."""
        if self.best_bid_price is not None and self.best_ask_price is not None:
            return round(self.best_ask_price - self.best_bid_price, 8)
        return None
    
    @property
    def midpoint(self) -> Optional[float]:
        """Calculate the current midpoint price."""
        if self.best_bid_price is not None and self.best_ask_price is not None:
            return round((self.best_bid_price + self.best_ask_price) / 2, 8)
        return None

    @property
    def question(self) -> str:
        """Get the market question."""
        return self.raw_data.get('question', '')

    @property
    def active(self) -> bool:
        """Check if the market is active."""
        return self.raw_data.get('active', True)

    @property
    def closed(self) -> bool:
        """Check if the market is closed."""
        return self.raw_data.get('closed', False)

    @property
    def volume_24h(self) -> float:
        """Get 24h trading volume."""
        return float(self.raw_data.get('volume24h', 0.0))

    @property
    def last_price(self) -> Optional[float]:
        """Get the last traded price."""
        price = self.raw_data.get('lastPrice')
        return float(price) if price is not None else None

class MarketDataService:
    """Service for ingesting and managing market data."""
    
    def __init__(
        self,
        client: ClobClient,
        update_interval: float = 1.0,  # seconds
        max_markets: int = 100
    ):
        """Initialize the market data service.
        
        Args:
            client: Authenticated Polymarket CLOB client
            update_interval: How often to refresh market data (seconds)
            max_markets: Maximum number of markets to track simultaneously
        """
        self.client = client
        self.update_interval = update_interval
        self.max_markets = max_markets
        
        # Internal state
        self._markets: Dict[str, MarketState] = {}  # condition_id -> MarketState
        self._token_to_market: Dict[str, str] = {}  # token_id -> condition_id
        self._running: bool = False
        self._tasks: Set[asyncio.Task] = set()
        self._callbacks: List[Callable[[str, MarketState], None]] = []
        
    async def start(self):
        """Start the market data service."""
        if self._running:
            logger.warning("Market data service is already running")
            return
            
        self._running = True
        logger.info("Starting market data service...")
        
        # Start the main update loop
        update_task = asyncio.create_task(self._update_loop())
        self._tasks.add(update_task)
        update_task.add_done_callback(self._tasks.discard)
        
        logger.info("Market data service started")
        
    async def stop(self):
        """Stop the market data service."""
        if not self._running:
            return
            
        self._running = False
        logger.info("Stopping market data service...")
        
        # Cancel all running tasks
        for task in self._tasks:
            task.cancel()
            
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
        
        logger.info("Market data service stopped")
        
    def add_callback(self, callback: Callable[[str, MarketState], None]):
        """Add a callback to be called when market state changes.
        
        Args:
            callback: Function to call with (condition_id, market_state) when updates occur
        """
        self._callbacks.append(callback)
        
    def get_market_state(self, condition_id: str) -> Optional[MarketState]:
        """Get the current state of a market.
        
        Args:
            condition_id: The market's condition ID
            
        Returns:
            The market state if found, None otherwise
        """
        return self._markets.get(condition_id)
        
    def get_all_markets(self) -> List[MarketState]:
        """Get states of all tracked markets.
        
        Returns:
            List of all market states
        """
        return list(self._markets.values())
        
    async def _update_loop(self):
        """Main loop for updating market data."""
        try:
            while self._running:
                try:
                    # Fetch active markets
                    markets = await self._fetch_markets()
                    
                    # Update internal state
                    await self._update_markets(markets)
                    
                    # Wait for next update
                    await asyncio.sleep(self.update_interval)
                    
                except Exception as e:
                    logger.error(f"Error in market update loop: {str(e)}")
                    await asyncio.sleep(self.update_interval)  # Still wait before retry
                    
        except asyncio.CancelledError:
            logger.info("Market update loop cancelled")
            raise
            
    async def _fetch_markets(self) -> List[Dict]:
        """Fetch active markets from Polymarket API with pagination."""
        all_markets = []
        next_cursor = None
        
        while True:
            try:
                response = await self.client.get_markets(cursor=next_cursor)
                
                if not isinstance(response, dict):
                    logger.error(f"Unexpected response format: {response}")
                    break
                    
                current_markets = response.get('data', [])
                if not current_markets:
                    logger.warning("No markets found in response")
                    break
                    
                # Log the first market's data for debugging
                if current_markets and len(all_markets) == 0:
                    first_market = current_markets[0]
                    market_info = {
                        'id': first_market.get('id'),
                        'question': first_market.get('question'),
                        'condition_id': first_market.get('conditionId'),
                        'tokens': [t.get('id') for t in first_market.get('tokens', [])],
                        'active': first_market.get('active'),
                        'closed': first_market.get('closed')
                    }
                    logger.info(f"Sample market data: {json.dumps(market_info, indent=2)}")
                
                all_markets.extend(current_markets)
                
                next_cursor = response.get('next_cursor')
                if not next_cursor or len(all_markets) >= self.max_markets:
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching markets: {e}")
                break
                
        logger.info(f"Fetched {len(all_markets)} markets")
        return all_markets[:self.max_markets]
        
    async def _update_markets(self, markets: List[Dict[str, Any]]) -> None:
        """Update the internal state of markets."""
        updated_markets = 0
        for market in markets:
            try:
                # Extract required fields
                market_id = market.get('id')
                if not market_id:
                    logging.warning("Market missing id")
                    continue

                condition_id = market.get('conditionId')
                if not condition_id:
                    logging.warning("Market missing condition_id")
                    continue

                tokens = market.get('tokens', [])
                if not tokens:
                    logging.warning(f"Market {market_id} has no tokens")
                    continue

                # Extract token IDs
                token_ids = []
                for token in tokens:
                    token_id = token.get('id')
                    if not token_id:
                        logging.warning(f"Token in market {market_id} missing id")
                        continue
                    token_ids.append(token_id)

                if not token_ids:
                    logging.warning(f"Market {market_id} has no valid token IDs")
                    continue

                # Try to get orderbook data for the first token (YES token)
                # But don't fail if orderbook doesn't exist
                best_bid_price = None
                best_ask_price = None
                try:
                    orderbook = await self.client.get_orderbook(token_ids[0])
                    if orderbook and 'bids' in orderbook and orderbook['bids']:
                        best_bid_price = float(orderbook['bids'][0]['price'])
                    if orderbook and 'asks' in orderbook and orderbook['asks']:
                        best_ask_price = float(orderbook['asks'][0]['price'])
                except Exception as e:
                    logging.debug(f"No orderbook for market {market_id}: {str(e)}")

                # Create or update MarketState
                market_state = MarketState(
                    market_id=market_id,
                    condition_id=condition_id,
                    token_ids=token_ids,
                    best_bid_price=best_bid_price,
                    best_ask_price=best_ask_price,
                    raw_data=market
                )

                # Update internal state
                self._markets[market_id] = market_state
                for token_id in token_ids:
                    self._token_to_market[token_id] = market_id

                updated_markets += 1

                # Notify callbacks
                for callback in self._callbacks:
                    try:
                        await callback(market_state)
                    except Exception as e:
                        logging.error(f"Error in market update callback: {str(e)}")

            except Exception as e:
                logging.error(f"Error updating market {market.get('id', 'unknown')}: {str(e)}")

        logging.info(f"Successfully updated {updated_markets} markets") 