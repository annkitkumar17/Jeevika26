import time
from typing import Tuple
from collections import defaultdict
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# In-memory fallback
_mem_rate_limit = defaultdict(list)

# Redis client if available
_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        try:
            import redis
            _redis_client = redis.Redis.from_url(
                settings.REDIS_URL,
                socket_connect_timeout=1,
                socket_timeout=1,
                decode_responses=True
            )
            _redis_client.ping()
        except Exception as e:
            _redis_client = False
            logger.info("Redis not available for rate limiter, using in-memory sliding window.")
    return _redis_client if _redis_client is not False else None

class RateLimiterService:
    @classmethod
    def check_rate_limit(cls, client_ip: str, limit: int = 100, window_seconds: int = 60) -> Tuple[bool, int]:
        """
        Returns (is_allowed, current_count)
        """
        redis_conn = get_redis_client()
        current_time = int(time.time())
        key = f"ratelimit:{client_ip}:{current_time // window_seconds}"
        
        if redis_conn:
            try:
                pipeline = redis_conn.pipeline()
                pipeline.incr(key)
                pipeline.expire(key, window_seconds * 2)
                results = pipeline.execute()
                count = results[0]
                return count <= limit, count
            except Exception:
                pass
                
        # Fallback to sliding window in memory
        now = time.time()
        _mem_rate_limit[client_ip] = [
            t for t in _mem_rate_limit[client_ip] if now - t < window_seconds
        ]
        if len(_mem_rate_limit[client_ip]) >= limit:
            return False, len(_mem_rate_limit[client_ip])
        _mem_rate_limit[client_ip].append(now)
        return True, len(_mem_rate_limit[client_ip])
