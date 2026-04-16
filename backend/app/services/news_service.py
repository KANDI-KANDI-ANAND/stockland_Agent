from backend.app.repositories.news_repository import NewsRepository


class NewsService:

    @staticmethod
    async def save_news(db, items):

        for item in items:

            await NewsRepository.upsert_news(
                db=db,
                location_id=item["location_id"],
                title=item["title"],
                summary=item["summary"],
                content=item["content"],
                link=item["link"],
                published_date=item["published_date"]
            )