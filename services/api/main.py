from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import redis.asyncio as redis
from loguru import logger
from ingest.config import IngestConfig
import json

app = FastAPI(title="Polybot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://3.65.249.159",
        "http://3.65.249.159:80",
        "http://3.65.249.159:3000",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración
config = IngestConfig()
redis_client = redis.from_url(config.REDIS_URL)

async def get_redis():
    """Dependency para obtener el cliente Redis."""
    return redis_client

@app.get("/api/markets")
async def get_markets(redis: redis.Redis = Depends(get_redis)):
    """Obtiene la lista de mercados activos."""
    try:
        markets = await redis.smembers("markets:active")
        return {"markets": [json.loads(market) for market in markets]}
    except Exception as e:
        logger.error(f"Failed to get markets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/markets/{market_id}")
async def get_market_details(market_id: str, redis: redis.Redis = Depends(get_redis)):
    """Obtiene detalles de un mercado específico."""
    try:
        market = await redis.get(f"market:{market_id}")
        if not market:
            raise HTTPException(status_code=404, detail="Market not found")
        return json.loads(market)
    except Exception as e:
        logger.error(f"Failed to get market details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/markets/{market_id}/events")
async def get_market_events(
    market_id: str,
    redis: redis.Redis = Depends(get_redis)
):
    """Obtiene eventos recientes de un mercado."""
    try:
        events = await redis.lrange(f"market:{market_id}:events", 0, -1)
        return {"events": [json.loads(event) for event in events]}
    except Exception as e:
        logger.error(f"Failed to get market events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats(redis: redis.Redis = Depends(get_redis)):
    """Obtiene estadísticas generales del bot."""
    try:
        stats = await redis.get("stats")
        if not stats:
            return {
                "totalMarkets": 0,
                "activeMarkets": 0,
                "totalVolume": 0,
                "totalTrades": 0
            }
        return json.loads(stats)
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check(redis: redis.Redis = Depends(get_redis)):
    """Verifica la salud del sistema."""
    try:
        await redis.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "redis": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 