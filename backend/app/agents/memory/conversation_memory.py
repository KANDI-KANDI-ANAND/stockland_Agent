from backend.app.core.redis_cache import redis_client

class ConversationMemory:
    def __init__(self, session_id: str):
        self.session_id = session_id

    def add_message(self, role, content):
        
        history = redis_client.get_history(self.session_id)
        
        
        history.append({
            "role": role,
            "content": content
        })
        
        
        redis_client.save_history(self.session_id, history)

    def get_history(self):
        return redis_client.get_history(self.session_id)
