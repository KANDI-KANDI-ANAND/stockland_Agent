import asyncio
import os
from sqlalchemy import text
from backend.app.database.connection import AsyncSessionLocal

async def check_data():
    async with AsyncSessionLocal() as db:
        h_total = await db.execute(text("SELECT count(*) FROM homes"))
        h_emb = await db.execute(text("SELECT count(*) FROM homes WHERE embedding IS NOT NULL"))
        l_total = await db.execute(text("SELECT count(*) FROM locations"))
        
        print("-" * 30)
        print(f"Total Homes on Render: {h_total.scalar()}")
        print(f"Homes with Embeddings: {h_emb.scalar()}")
        print(f"Total Locations on Render: {l_total.scalar()}")
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(check_data())
