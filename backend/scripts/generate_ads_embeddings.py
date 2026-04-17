import asyncio
from sqlalchemy import select

from backend.app.database.connection import AsyncSessionLocal
from backend.app.database.models.ads import Ad
from backend.app.services.embedding_service import EmbeddingService

def build_summary(ad: Ad):


    parts = []

    if ad.start_date:
        parts.append(f"Advertisement started on {ad.start_date}")

    if ad.ad_text:
        parts.append(ad.ad_text)

    summary = ". ".join(parts)

    return summary


async def main():


    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Ad)
        )

        ads = result.scalars().all()

        print("Total ads:", len(ads))

        for ad in ads:

            if ad.embedding is not None:
                continue

            summary = build_summary(ad)

            embedding = EmbeddingService.generate_embedding(summary)

            ad.summary = summary
            ad.embedding = embedding

            print("Embedded ad:", ad.id)

        await db.commit()

        print("Ads embeddings generated successfully")


if __name__ == "__main__":
    asyncio.run(main())
