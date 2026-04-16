from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.models.ads import Ad


class AdsRepository:

    @staticmethod
    async def get_by_location(db, community_name):

        query = text("""
        SELECT ads.*
        FROM ads
        JOIN locations ON ads.location_id = locations.id
        WHERE LOWER(locations.name) LIKE LOWER(:community)
        LIMIT 5
        """)

        result = await db.execute(
            query,
            {"community": f"%{community_name}%"}
        )

        return result.mappings().all()

    
    @staticmethod
    async def upsert_ad(
        db: AsyncSession,
        location_id: int,
        ad_text: str,
        image_url: str | None,
        start_date: str | None
    ):

        query = select(Ad).where(
            Ad.ad_text == ad_text
        )

        result = await db.execute(query)

        existing = result.scalar_one_or_none()

        if not existing:

            ad = Ad(
                location_id=location_id,
                ad_text=ad_text,
                image_url=image_url,
                start_date=start_date
            )

            db.add(ad)

            return ad

        changed = False

        if existing.image_url != image_url:
            existing.image_url = image_url
            changed = True

        if existing.start_date != start_date:
            existing.start_date = start_date
            changed = True

        if existing.location_id != location_id:
            existing.location_id = location_id
            changed = True

        if changed:
            existing.summary = None
            existing.embedding = None
            print("Updated ad")

        return existing

        ad = Ad(
            location_id=location_id,
            ad_text=ad_text,
            image_url=image_url,
            start_date=start_date
        )

        db.add(ad)

        return ad