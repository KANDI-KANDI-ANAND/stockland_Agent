import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

class RedisCache:
    def __init__(self):
        # FIX: Try to get REDIS_URL from Render, otherwise fallback to localhost
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # We use from_url because Render provides the connection as a full URL
        self.client = redis.from_url(redis_url, decode_responses=True)

    def save_history(self, session_id: str, history: list):
        key = f"chat_history:{session_id}"
        self.client.set(key, json.dumps(history))

    def get_history(self, session_id: str):
        key = f"chat_history:{session_id}"
        data = self.client.get(key)
        return json.loads(data) if data else []

    def clear_history(self, session_id: str):
        key = f"chat_history:{session_id}"
        self.client.delete(key)

    def set_cache(self, key: str, value: str, ttl: int = 86400):
        self.client.set(key, value, ex=ttl)

    def get_cache(self, key: str):
        return self.client.get(key)

# Global instance
redis_client = RedisCache()
