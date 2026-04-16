from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.models.release import Release


class ReleaseRepository:

    @staticmethod
    async def upsert_release(
        db: AsyncSession,
        location_id: int,
        title: str,
        status: str,
        description: str,
        link: str | None,
        image_url: str | None
    ):

        query = select(Release).where(
            Release.location_id == location_id,
            Release.title == title
        )

        result = await db.execute(query)

        existing = result.scalar_one_or_none()

        if not existing:

            release = Release(
                location_id=location_id,
                title=title,
                status=status,
                description=description,
                link=link,
                image_url=image_url
            )

            db.add(release)

            return release

        changed = False

        if existing.status != status:
            existing.status = status
            changed = True

        if existing.description != description:
            existing.description = description
            changed = True

        if existing.link != link:
            existing.link = link
            changed = True

        if existing.image_url != image_url:
            existing.image_url = image_url
            changed = True

        if changed:
            existing.summary = None
            existing.embedding = None
            print("Updated release:", title)

        return existing

        release = Release(
            location_id=location_id,
            title=title,
            status=status,
            description=description,
            link=link,
            image_url=image_url
        )

        db.add(release)

        return release