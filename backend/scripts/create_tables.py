import asyncio

from backend.app.database.connection import engine, Base
from backend.app.database import models


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())