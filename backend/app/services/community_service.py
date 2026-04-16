from backend.app.repositories.location_repository import LocationRepository


class CommunityService:

    @staticmethod
    async def save_communities(db, communities):

        for c in communities:

            await LocationRepository.upsert_location(
                db,
                name=c["name"],
                state=c["state"],
                url=c["url"],
                description=c["description"],
                amenities=c["amenities"]
            )