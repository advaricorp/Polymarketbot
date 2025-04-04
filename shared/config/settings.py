import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

# API Credentials
POLY_PRIVATE_KEY = os.getenv("POLY_PRIVATE_KEY")
POLY_API_KEY = os.getenv("POLY_API_KEY")
POLY_API_SECRET = os.getenv("POLY_API_SECRET")
POLY_PASSPHRASE = os.getenv("POLY_PASSPHRASE")

# API Endpoints
POLY_WS_URL = os.getenv("POLY_WS_URL", "wss://clob.polymarket.com/ws")
POLY_REST_URL = os.getenv("POLY_REST_URL", "https://clob.polymarket.com")

# Database URLs
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost:5432/polybot")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Vector DB
CHROMA_DB_PATH = Path(os.getenv("CHROMA_DB_PATH", "./data/vector_db"))
CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_PATH = Path(os.getenv("LOG_PATH", "./data/logs/polybot.log"))
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
