from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pgvector.sqlalchemy import Vector

from backend.app.database.models.location import Location


class VectorRepository:

    @staticmethod
    async def search_locations_by_embedding(
        db: AsyncSession,
        query_embedding: list[float],
        limit: int = 5
    ):
        """
        Perform vector similarity search on locations table
        """

        query = (
            select(Location)
            .order_by(Location.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )

        result = await db.execute(query)

        return result.scalars().all()