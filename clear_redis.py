import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url)

try:
    r.flushall()
    print("✅ Redis Cache cleared successfully!")
except Exception as e:
    print(f"❌ Error clearing Redis: {e}")
