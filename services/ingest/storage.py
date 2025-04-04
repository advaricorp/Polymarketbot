import json
from typing import Dict, Any, Optional
import redis.asyncio as redis
from loguru import logger
from .config import IngestConfig

class EventStorage:
    """Clase para manejar el almacenamiento de eventos en Redis."""
    
    def __init__(self, config: IngestConfig):
        self.config = config
        self.redis: Optional[redis.Redis] = None
        self.connected = False
        
    async def connect(self) -> None:
        """Establece la conexión con Redis."""
        try:
            self.redis = redis.from_url(self.config.REDIS_URL)
            await self.redis.ping()  # Verificar conexión
            self.connected = True
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.connected = False
            raise
    
    async def publish_event(self, channel: str, event: Dict[str, Any]) -> None:
        """Publica un evento en un canal específico."""
        if not self.connected or not self.redis:
            raise ConnectionError("Redis not connected")
            
        try:
            # Serializar el evento a JSON
            event_json = json.dumps(event)
            
            # Publicar en Redis
            await self.redis.publish(channel, event_json)
            logger.debug(f"Published event to channel {channel}: {event}")
            
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            raise
    
    async def store_event(self, key: str, event: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """Almacena un evento en Redis con una clave específica."""
        if not self.connected or not self.redis:
            raise ConnectionError("Redis not connected")
            
        try:
            # Serializar el evento a JSON
            event_json = json.dumps(event)
            
            # Almacenar en Redis
            await self.redis.set(key, event_json)
            
            # Establecer TTL si se especifica
            if ttl:
                await self.redis.expire(key, ttl)
                
            logger.debug(f"Stored event with key {key}: {event}")
            
        except Exception as e:
            logger.error(f"Failed to store event: {e}")
            raise
    
    async def get_event(self, key: str) -> Optional[Dict[str, Any]]:
        """Recupera un evento almacenado por su clave."""
        if not self.connected or not self.redis:
            raise ConnectionError("Redis not connected")
            
        try:
            # Obtener el evento de Redis
            event_json = await self.redis.get(key)
            if not event_json:
                return None
                
            # Deserializar el evento
            return json.loads(event_json)
            
        except Exception as e:
            logger.error(f"Failed to get event: {e}")
            raise
    
    async def close(self) -> None:
        """Cierra la conexión con Redis."""
        if self.redis:
            await self.redis.close()
            self.connected = False
            logger.info("Redis connection closed") 