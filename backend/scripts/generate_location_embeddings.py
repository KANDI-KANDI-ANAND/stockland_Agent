import asyncio
from sqlalchemy import select

from backend.app.database.connection import AsyncSessionLocal
from backend.app.database.models.location import Location
from backend.app.services.embedding_service import EmbeddingService


def build_summary(location):

    amenities = ", ".join(location.amenities) if location.amenities else ""

    return f"""
{location.name} is a residential community in {location.state}.
{location.description}
Amenities available include {amenities}.
""".strip()


async def main():

    async with AsyncSessionLocal() as db:

        result = await db.execute(select(Location))
        locations = result.scalars().all()

        print("Total locations:", len(locations))

        for location in locations:
            summary = build_summary(location)
            embedding = EmbeddingService.generate_embedding(summary)
            
            location.summary = summary
            location.embedding = embedding
            print(f"Updated: {location.name}")
        await db.commit()
    print("Location embeddings updated successfully.")
if __name__ == "__main__":
    asyncio.run(main())