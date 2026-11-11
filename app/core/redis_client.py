from redis import Redis
from redis.backoff import NoBackoff
from redis.retry import Retry

from app.core.config import REDIS_URL

redis_client = (
    Redis.from_url(
        REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=0.25,
        socket_timeout=0.25,
        retry=Retry(NoBackoff(), 0),
    )
    if REDIS_URL
    else None
)