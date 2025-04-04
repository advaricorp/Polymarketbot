from typing import Dict, List
from pydantic_settings import BaseSettings

class IngestConfig(BaseSettings):
    """Configuración del servicio de ingesta."""
    
    # URLs y endpoints
    POLY_WS_URL: str = "wss://clob.polymarket.com/ws"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Canales de WebSocket a suscribir
    WS_CHANNELS: List[str] = [
        "l2_book",  # Libro de órdenes
        "trades",   # Operaciones ejecutadas
        "ticker",   # Resumen de mercado
        "markets"   # Información de mercados
    ]
    
    # Configuración de reconexión
    RECONNECT_DELAY: int = 5  # segundos
    MAX_RECONNECT_ATTEMPTS: int = 10
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    
    # Configuración de validación
    MAX_MESSAGE_SIZE: int = 1024 * 1024  # 1MB
    ALLOWED_EVENT_TYPES: List[str] = [
        "subscribe",
        "unsubscribe",
        "l2_book",
        "trades",
        "ticker",
        "markets",
        "error"
    ]
    
    class Config:
        env_prefix = "INGEST_" 