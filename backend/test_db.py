import asyncio
from sqlalchemy import text
from app.database.connection import engine


async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("Database connected:", result.scalar())


asyncio.run(test_connection())