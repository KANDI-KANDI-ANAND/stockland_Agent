from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.models.location import Location


class LocationRepository:

    @staticmethod
    async def get_by_name(db, name):

        query = text("""
        SELECT *
        FROM locations
        WHERE LOWER(name) LIKE LOWER(:name)
        LIMIT 1
        """)

        result = await db.execute(query, {"name": f"%{name}%"})

        return result.mappings().first()

    @staticmethod
    async def upsert_location(
        db,
        name: str,
        state: str,
        url: str,
        description: str,
        amenities: list | None = None,
    ):

        query = select(Location).where(
            Location.name == name,
            Location.state == state
        )

        result = await db.execute(query)

        existing = result.scalar_one_or_none()

        if not existing:

            location = Location(
                name=name,
                state=state,
                url=url,
                description=description,
                amenities=amenities,
            )

            db.add(location)

            return location

        changed = False

        if existing.description != description:
            existing.description = description
            changed = True

        if existing.amenities != amenities:
            existing.amenities = amenities
            changed = True

        if existing.url != url:
            existing.url = url
            changed = True

        if changed:
            existing.summary = None
            existing.embedding = None
            print(f"Updated: {name}")

        return existing


    @staticmethod
    async def get_all_locations(db: AsyncSession):

        query = select(Location)

        result = await db.execute(query)

        return result.scalars().all()


    @staticmethod
    async def get_locations_by_state(db: AsyncSession, state: str):

        query = select(Location).where(Location.state == state)

        result = await db.execute(query)

        return result.scalars().all()


    @staticmethod
    async def get_location_by_id(db: AsyncSession, location_id: int):

        query = select(Location).where(Location.id == location_id)

        result = await db.execute(query)

        return result.scalar_one_or_none()


    @staticmethod
    async def semantic_search(db, embedding, limit=5):

        embedding_str = "[" + ",".join(map(str, embedding)) + "]"

        query = text("""
        SELECT id, name, state, description, amenities, url
        FROM locations
        ORDER BY embedding <-> CAST(:embedding AS vector)
        LIMIT :limit
        """)

        result = await db.execute(
            query,
            {
                "embedding": embedding_str,
                "limit": limit
            }
        )

        rows = result.fetchall()

        return [
            {
                "id": r.id,
                "name": r.name,
                "state": r.state,
                "description": r.description,
                "amenities": r.amenities,
                "url": r.url,
            }
            for r in rows
        ]   