import asyncio
import json
from typing import Dict, Any
import websockets
from fastapi import FastAPI, WebSocket
from loguru import logger
import redis.asyncio as redis
from shared.config.settings import POLY_WS_URL, REDIS_URL

# Configurar logger
logger.add("data/logs/ingest.log", rotation="1 day")

app = FastAPI(title="Polybot Ingest Service")
redis_client = redis.from_url(REDIS_URL)

async def connect_to_polymarket():
    """Conecta al WebSocket de Polymarket y procesa los mensajes."""
    while True:
        try:
            async with websockets.connect(POLY_WS_URL) as websocket:
                logger.info("Connected to Polymarket WebSocket")
                
                # Suscribirse a los eventos de mercado
                subscribe_message = {
                    "type": "subscribe",
                    "channel": "l2_book",
                    "market": "all"
                }
                await websocket.send(json.dumps(subscribe_message))
                
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    # Publicar el mensaje en Redis para otros servicios
                    await redis_client.publish("market_events", json.dumps(data))
                    logger.debug(f"Published event: {data}")
                    
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            await asyncio.sleep(5)  # Esperar antes de reconectar

@app.on_event("startup")
async def startup_event():
    """Inicia la conexión WebSocket al arrancar el servicio."""
    asyncio.create_task(connect_to_polymarket())

@app.get("/health")
async def health_check():
    """Endpoint de healthcheck."""
    return {"status": "healthy"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para clientes que quieran recibir eventos en tiempo real."""
    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("market_events")
    
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_text(message["data"].decode())
    except Exception as e:
        logger.error(f"WebSocket client error: {e}")
    finally:
        await pubsub.unsubscribe()
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
