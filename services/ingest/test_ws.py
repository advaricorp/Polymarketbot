#!/usr/bin/env python3
import asyncio
import websockets
import json
import sys
from loguru import logger

async def test_websocket():
    """Prueba la conexión al WebSocket de Polymarket."""
    uri = "wss://clob.polymarket.com/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to Polymarket WebSocket")
            
            # Suscribirse a los eventos de mercado
            subscribe_message = {
                "type": "subscribe",
                "channel": "l2_book",
                "market": "all"
            }
            await websocket.send(json.dumps(subscribe_message))
            logger.info("Sent subscription message")
            
            # Recibir y mostrar mensajes
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                logger.info(f"Received: {json.dumps(data, indent=2)}")
                
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logger.add(sys.stderr, level="INFO")
    asyncio.run(test_websocket()) 