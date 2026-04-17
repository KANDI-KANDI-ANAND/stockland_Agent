import asyncio

from sqlalchemy import select

from backend.app.database.connection import AsyncSessionLocal
from backend.app.database.models.news import News
from backend.app.services.embedding_service import EmbeddingService


async def main():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(News)
        )

        news_list = result.scalars().all()

        print("Total news:", len(news_list))

        for news in news_list:

            if news.embedding is not None:
                continue

            text = f"{news.title}. {news.summary}. {news.published_date}"

            embedding = EmbeddingService.generate_embedding(text)

            news.embedding = embedding

            print("Embedded:", news.id)

        await db.commit()

        print("Embeddings generated successfully")


if __name__ == "__main__":
    asyncio.run(main())