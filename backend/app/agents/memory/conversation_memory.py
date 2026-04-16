from backend.app.core.redis_cache import redis_client

class ConversationMemory:
    def __init__(self, session_id: str):
        self.session_id = session_id

    def add_message(self, role, content):
        # 1. Get current history from Redis
        history = redis_client.get_history(self.session_id)
        
        # 2. Append new message
        history.append({
            "role": role,
            "content": content
        })
        
        # 3. Save back to Redis
        redis_client.save_history(self.session_id, history)

    def get_history(self):
        return redis_client.get_history(self.session_id)
