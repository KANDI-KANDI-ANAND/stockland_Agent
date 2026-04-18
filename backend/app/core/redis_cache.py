import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

class RedisCache:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL")
        
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


redis_client = RedisCache()
