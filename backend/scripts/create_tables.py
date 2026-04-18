import asyncio
from sqlalchemy import text
from backend.app.database.connection import engine, Base
from backend.app.database import models

async def create_tables():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully on Render!")

if __name__ == "__main__":
    asyncio.run(create_tables())
