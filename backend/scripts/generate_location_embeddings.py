import asyncio
from sqlalchemy import select

from backend.app.database.connection import AsyncSessionLocal
from backend.app.database.models.location import Location
from backend.app.core.embedding_model import model


def build_summary(location):

    amenities = ", ".join(location.amenities) if location.amenities else ""

    return f"""
{location.name} is a residential community in {location.state}.
{location.description}
Amenities available include {amenities}.
""".strip()


def generate_embeddings_batch(texts):
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


async def main():

    async with AsyncSessionLocal() as db:

        result = await db.execute(select(Location))
        locations = result.scalars().all()

        print("Total locations:", len(locations))

        summaries = []
        location_ids = []

        for location in locations:

            summary = build_summary(location)

            summaries.append(summary)
            location_ids.append(location.id)

        embeddings = generate_embeddings_batch(summaries)

        for i, location in enumerate(locations):

            location.summary = summaries[i]
            location.embedding = embeddings[i]

            print("Updated:", location.name)

        await db.commit()

    print("Embeddings generated successfully.")


if __name__ == "__main__":
    asyncio.run(main())