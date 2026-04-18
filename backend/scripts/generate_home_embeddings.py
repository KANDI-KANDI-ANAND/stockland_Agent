import asyncio
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from backend.app.database.connection import AsyncSessionLocal
from backend.app.database.models.home import Home
from backend.app.services.embedding_service import EmbeddingService


def build_summary(home: Home):
    parts = []

    location_name = home.location.name if home.location else "Unknown Community"
    location_state = home.location.state if home.location else "Unknown State"
    
    parts.append(f"Located in the {location_name} community in {location_state}")

    if home.home_type:
        parts.append(home.home_type)

    if home.bedrooms:
        parts.append(f"{home.bedrooms} bedrooms")

    if home.bathrooms:
        parts.append(f"{home.bathrooms} bathrooms")

    if home.size:
        parts.append(f"{home.size} square metres")

    if home.price:
        parts.append(f"priced at ${int(home.price)}")

    summary = "This home offers " + ", ".join(parts) + "."
    return summary


async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Home).options(joinedload(Home.location))
        )

        homes = result.scalars().all()
        print("Total homes to process:", len(homes))

        for home in homes:
            summary = build_summary(home)
            embedding = EmbeddingService.generate_embedding(summary)

            home.summary = summary
            home.embedding = embedding
            print(f"Updated: {home.home_type} in {home.location.state if home.location else ''}")

        await db.commit()
        print("\nHome embeddings with context generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
