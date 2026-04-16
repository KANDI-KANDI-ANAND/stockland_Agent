import redis
import json

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def save_history(self, session_id: str, history: list):
        """Save chat history for a specific session"""
        key = f"chat_history:{session_id}"
        self.client.set(key, json.dumps(history))

    def get_history(self, session_id: str):
        """Retrieve chat history for a specific session"""
        key = f"chat_history:{session_id}"
        data = self.client.get(key)
        return json.loads(data) if data else []

    def clear_history(self, session_id: str):
        key = f"chat_history:{session_id}"
        self.client.delete(key)

    def set_cache(self, key: str, value: str, ttl: int = 86400):
        """Store a value with a Time-To-Live (Default: 24 hours)"""
        self.client.set(key, value, ex=ttl)

    def get_cache(self, key: str):
        """Retrieve a cached value"""
        return self.client.get(key)

# Global instance
redis_client = RedisCache()
