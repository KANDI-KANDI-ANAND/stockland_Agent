from sqlalchemy import select, text
from backend.app.database.models.news import News


class NewsRepository:

    @staticmethod
    async def get_by_location(db, community_name):

        query = text("""
        SELECT news.*
        FROM news
        JOIN locations ON news.location_id = locations.id
        WHERE LOWER(locations.name) LIKE LOWER(:community)
        ORDER BY news.created_at DESC
        LIMIT 5
        """)

        result = await db.execute(
            query,
            {"community": f"%{community_name}%"}
        )

        return result.mappings().all()

    @staticmethod
    async def upsert_news(db, location_id, title, summary, content, link, published_date):

        query = select(News).where(
            News.link == link
        )

        result = await db.execute(query)

        existing = result.scalar_one_or_none()

        if not existing:

            news = News(
                location_id=location_id,
                title=title,
                summary=summary,
                content=content,
                link=link,
                published_date=published_date
            )

            db.add(news)

            return news

        changed = False

        if existing.title != title:
            existing.title = title
            changed = True

        if existing.summary != summary:
            existing.summary = summary
            changed = True

        if existing.content != content:
            existing.content = content
            changed = True

        if existing.published_date != published_date:
            existing.published_date = published_date
            changed = True

        if changed:
            existing.summary = None
            existing.embedding = None
            print("Updated news:", title)

        return existing

        news = News(
            location_id=location_id,
            title=title,
            summary=summary,
            content=content,
            link=link,
            published_date=published_date
        )

        db.add(news)

        return news