import asyncio
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, HTTPException
from loguru import logger
from .config import IngestConfig
from .websocket import PolymarketWebSocket
from .storage import EventStorage

# Configurar logger
logger.add(
    "data/logs/ingest.log",
    rotation="1 day",
    level=IngestConfig().LOG_LEVEL,
    format=IngestConfig().LOG_FORMAT
)

app = FastAPI(title="Polybot Ingest Service")

# Instancias globales
config = IngestConfig()
websocket_client = PolymarketWebSocket(config)
event_storage = EventStorage(config)

async def handle_market_event(event: Dict[str, Any]) -> None:
    """Maneja eventos de mercado."""
    try:
        # Publicar el evento en Redis
        await event_storage.publish_event("market_events", event)
        
        # Almacenar el evento para análisis posterior
        event_id = f"market:{event.get('market', 'unknown')}:{event.get('timestamp', '')}"
        await event_storage.store_event(event_id, event, ttl=86400)  # 24 horas TTL
        
    except Exception as e:
        logger.error(f"Error handling market event: {e}")

@app.on_event("startup")
async def startup_event():
    """Inicia las conexiones al arrancar el servicio."""
    try:
        # Conectar a Redis
        await event_storage.connect()
        
        # Configurar manejadores de eventos
        websocket_client.register_handler("l2_book", handle_market_event)
        websocket_client.register_handler("trades", handle_market_event)
        websocket_client.register_handler("ticker", handle_market_event)
        websocket_client.register_handler("markets", handle_market_event)
        
        # Iniciar conexión WebSocket y escucha
        await websocket_client.connect()
        asyncio.create_task(websocket_client.listen())
        
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cierra las conexiones al detener el servicio."""
    try:
        await websocket_client.close()
        await event_storage.close()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

@app.get("/health")
async def health_check():
    """Endpoint de healthcheck."""
    try:
        # Verificar conexiones
        if not websocket_client.connected:
            raise HTTPException(status_code=503, detail="WebSocket not connected")
        if not event_storage.connected:
            raise HTTPException(status_code=503, detail="Redis not connected")
            
        return {
            "status": "healthy",
            "websocket_connected": websocket_client.connected,
            "redis_connected": event_storage.connected,
            "reconnect_attempts": websocket_client.reconnect_attempts
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para clientes que quieran recibir eventos en tiempo real."""
    await websocket.accept()
    
    try:
        # Crear un pubsub para este cliente
        pubsub = event_storage.redis.pubsub()
        await pubsub.subscribe("market_events")
        
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_text(message["data"].decode())
                
    except Exception as e:
        logger.error(f"WebSocket client error: {e}")
    finally:
        await pubsub.unsubscribe()
        await websocket.close()

@app.get("/events/{market_id}")
async def get_market_events(market_id: str):
    """Recupera eventos almacenados para un mercado específico."""
    try:
        # Buscar eventos por prefijo de mercado
        pattern = f"market:{market_id}:*"
        keys = await event_storage.redis.keys(pattern)
        
        events = []
        for key in keys:
            event = await event_storage.get_event(key)
            if event:
                events.append(event)
                
        return {"market_id": market_id, "events": events}
        
    except Exception as e:
        logger.error(f"Failed to get market events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
