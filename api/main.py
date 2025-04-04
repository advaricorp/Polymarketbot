"""
FastAPI application for the Polymarket Bot API.
"""

import os
import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
import logging

from services.ingest.market_data import MarketState, MarketDataService

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Polymarket Bot API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instance
market_data_service = None

# Pydantic models for API responses
class MarketStateResponse(BaseModel):
    condition_id: str
    question: str
    token_ids: List[str]
    active: bool
    closed: bool
    best_bid: Optional[float] = None
    best_ask: Optional[float] = None
    last_price: Optional[float] = None
    last_update: str
    volume_24h: float
    spread: Optional[float] = None
    midpoint: Optional[float] = None

    class Config:
        from_attributes = True

# Dependency to get the market data service
async def get_market_service():
    global market_data_service
    if market_data_service is None:
        # Initialize the service if it doesn't exist
        host = os.getenv("POLYMARKET_API_HOST")
        api_key = os.getenv("POLYMARKET_API_KEY")
        api_secret = os.getenv("POLYMARKET_API_SECRET")
        api_passphrase = os.getenv("POLYMARKET_API_PASSPHRASE")
        private_key = os.getenv("POLY_PRIVATE_KEY")
        
        # Debug log environment variables
        logger.info("Environment variables:")
        logger.info(f"POLYMARKET_API_HOST: {host}")
        logger.info(f"POLYMARKET_API_KEY: {'*' * len(api_key) if api_key else 'None'}")
        logger.info(f"POLYMARKET_API_SECRET: {'*' * len(api_secret) if api_secret else 'None'}")
        logger.info(f"POLYMARKET_API_PASSPHRASE: {'*' * len(api_passphrase) if api_passphrase else 'None'}")
        logger.info(f"POLY_PRIVATE_KEY: {'*' * len(private_key) if private_key else 'None'}")
        
        if not all([host, api_key, api_secret, api_passphrase, private_key]):
            logger.error("Missing required environment variables for Polymarket API")
            raise ValueError("Missing required environment variables for Polymarket API")
        
        # Add 0x prefix to private key if missing
        if not private_key.startswith("0x"):
            private_key = "0x" + private_key
        
        logger.info("Initializing Polymarket client...")
        client = ClobClient(
            host=host,
            key=private_key,
            chain_id=137,  # Polygon mainnet
            creds=ApiCreds(
                api_key=api_key,
                api_secret=api_secret,
                api_passphrase=api_passphrase
            )
        )
        
        logger.info("Initializing market data service...")
        market_data_service = MarketDataService(client)
        
        # Start the service
        await market_data_service.start()
    
    return market_data_service

@app.on_event("startup")
async def startup_event():
    """Start the market data service when the API server starts."""
    logger.info("Starting market data service...")
    await get_market_service()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the market data service when the API server stops."""
    logger.info("Stopping market data service...")
    global market_data_service
    if market_data_service is not None:
        await market_data_service.stop()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/markets", response_model=List[MarketStateResponse])
async def get_markets(service: MarketDataService = Depends(get_market_service)):
    """Get all markets."""
    markets = service.get_all_markets()
    logger.info(f"Returning {len(markets)} markets")
    return markets

@app.get("/markets/{condition_id}", response_model=MarketStateResponse)
async def get_market(
    condition_id: str,
    service: MarketDataService = Depends(get_market_service)
):
    """Get a specific market by condition ID."""
    market = service.get_market_state(condition_id)
    if market is None:
        logger.warning(f"Market not found: {condition_id}")
        raise HTTPException(status_code=404, detail="Market not found")
    logger.info(f"Returning market data for {condition_id}")
    return market

@app.post("/markets/refresh")
async def refresh_markets(service: MarketDataService = Depends(get_market_service)):
    """Force a refresh of market data."""
    logger.info("Refreshing market data...")
    await service.stop()
    await service.start()
    logger.info("Market data service restarted")
    return {"status": "ok", "message": "Market data service restarted"} 