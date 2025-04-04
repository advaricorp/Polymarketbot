import asyncio
import json
from typing import Dict, Any, Optional
import websockets
from loguru import logger
from .config import IngestConfig

class PolymarketWebSocket:
    """Clase para manejar la conexión WebSocket con Polymarket."""
    
    def __init__(self, config: IngestConfig):
        self.config = config
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.connected = False
        self.reconnect_attempts = 0
        self._message_handlers = {}
        
    async def connect(self) -> None:
        """Establece la conexión WebSocket con Polymarket."""
        try:
            self.ws = await websockets.connect(self.config.POLY_WS_URL)
            self.connected = True
            self.reconnect_attempts = 0
            logger.info("Connected to Polymarket WebSocket")
            
            # Suscribirse a todos los canales configurados
            for channel in self.config.WS_CHANNELS:
                await self.subscribe(channel)
                
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            self.connected = False
            raise
    
    async def subscribe(self, channel: str) -> None:
        """Suscribe a un canal específico."""
        if not self.connected or not self.ws:
            raise ConnectionError("WebSocket not connected")
            
        subscribe_message = {
            "type": "subscribe",
            "channel": channel,
            "market": "all"
        }
        await self.ws.send(json.dumps(subscribe_message))
        logger.info(f"Subscribed to channel: {channel}")
    
    async def unsubscribe(self, channel: str) -> None:
        """Cancela la suscripción a un canal."""
        if not self.connected or not self.ws:
            raise ConnectionError("WebSocket not connected")
            
        unsubscribe_message = {
            "type": "unsubscribe",
            "channel": channel,
            "market": "all"
        }
        await self.ws.send(json.dumps(unsubscribe_message))
        logger.info(f"Unsubscribed from channel: {channel}")
    
    def register_handler(self, event_type: str, handler: callable) -> None:
        """Registra un manejador para un tipo específico de evento."""
        self._message_handlers[event_type] = handler
    
    async def _handle_message(self, message: str) -> None:
        """Procesa un mensaje recibido."""
        try:
            data = json.loads(message)
            
            # Validar el tipo de evento
            event_type = data.get("type")
            if event_type not in self.config.ALLOWED_EVENT_TYPES:
                logger.warning(f"Received unknown event type: {event_type}")
                return
                
            # Llamar al manejador correspondiente si existe
            if event_type in self._message_handlers:
                await self._message_handlers[event_type](data)
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message: {e}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def _reconnect(self) -> None:
        """Intenta reconectar al WebSocket."""
        if self.reconnect_attempts >= self.config.MAX_RECONNECT_ATTEMPTS:
            logger.error("Max reconnection attempts reached")
            return
            
        self.reconnect_attempts += 1
        logger.info(f"Attempting to reconnect ({self.reconnect_attempts}/{self.config.MAX_RECONNECT_ATTEMPTS})")
        
        try:
            await self.connect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")
            await asyncio.sleep(self.config.RECONNECT_DELAY)
            await self._reconnect()
    
    async def listen(self) -> None:
        """Escucha mensajes del WebSocket."""
        while True:
            try:
                if not self.connected or not self.ws:
                    await self._reconnect()
                    continue
                    
                message = await self.ws.recv()
                await self._handle_message(message)
                
            except websockets.ConnectionClosed:
                logger.warning("WebSocket connection closed")
                self.connected = False
                await self._reconnect()
            except Exception as e:
                logger.error(f"Error in WebSocket listener: {e}")
                self.connected = False
                await self._reconnect()
    
    async def close(self) -> None:
        """Cierra la conexión WebSocket."""
        if self.ws:
            await self.ws.close()
            self.connected = False
            logger.info("WebSocket connection closed") 