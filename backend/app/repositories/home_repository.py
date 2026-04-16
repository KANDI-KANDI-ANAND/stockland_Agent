from sqlalchemy import select, text
from backend.app.database.models.home import Home


class HomeRepository:

    @staticmethod
    async def get_by_location(db, community_name):

        query = text("""
        SELECT homes.*
        FROM homes
        JOIN locations ON homes.location_id = locations.id
        WHERE LOWER(locations.name) LIKE LOWER(:community)
        LIMIT 10
        """)

        result = await db.execute(
            query,
            {"community": f"%{community_name}%"}
        )

        return result.mappings().all()

    @staticmethod
    async def upsert_home(
        db,
        location_id,
        home_type,
        price,
        bedrooms,
        bathrooms,
        size,
        image_url
    ):

        query = select(Home).where(
            Home.location_id == location_id,
            Home.home_type == home_type
        )

        result = await db.execute(query)

        existing = result.scalar_one_or_none()

        if not existing:

            home = Home(
                location_id=location_id,
                home_type=home_type,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                size=size,
                image_url=image_url
            )

            db.add(home)

            return home

        changed = False

        if existing.price != price:
            existing.price = price
            changed = True

        if existing.bedrooms != bedrooms:
            existing.bedrooms = bedrooms
            changed = True

        if existing.bathrooms != bathrooms:
            existing.bathrooms = bathrooms
            changed = True

        if existing.size != size:
            existing.size = size
            changed = True

        if existing.image_url != image_url:
            existing.image_url = image_url
            changed = True

        if changed:
            existing.summary = None
            existing.embedding = None
            print("Updated:", home_type)

        return existing