from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / '.env')

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

if len(JWT_SECRET_KEY.encode('utf-8')) < 32:
    raise ValueError(
        'JWT_SECRET_KEY must be at least 32 bytes'
    )

if JWT_ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
    raise ValueError("JWT token expiry must be greater than zero")

REDIS_URL = os.getenv("REDIS_URL", "").strip()
AUTH_CACHE_TTL_SECONDS = int(os.getenv("AUTH_CACHE_TTL_SECONDS", "60"))
AUTH_CACHE_KEY_PREFIX = os.getenv(
    "AUTH_CACHE_KEY_PREFIX",
    f"learning-fastapi:{os.getenv('DB_NAME', 'fastapi_learning')}:auth:v1",
)
