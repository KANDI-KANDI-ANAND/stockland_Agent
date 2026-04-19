import asyncio
from sqlalchemy import select

from backend.app.database.connection import AsyncSessionLocal
from backend.app.database.models.release import Release
from backend.app.services.embedding_service import EmbeddingService

def build_summary(release: Release):

    parts = []

    if release.title:
        parts.append(f"Construction update: {release.title}")

    if release.status:
        parts.append(f"Status: {release.status}")

    if release.description:
        parts.append(release.description)

    return ". ".join(parts)


async def main():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Release)
        )

        releases = result.scalars().all()

        print("Total releases:", len(releases))

        for release in releases:

            if release.embedding is not None:
                continue

            summary = build_summary(release)

            embedding = EmbeddingService.generate_embedding(summary)

            release.summary = summary
            release.embedding = embedding

            print("Embedded release:", release.id)

        await db.commit()

        print("Release embeddings generated successfully")


if __name__ == "__main__":
    asyncio.run(main())
