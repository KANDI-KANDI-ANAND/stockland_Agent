from backend.app.repositories.release_repository import ReleaseRepository


class ReleaseService:

    @staticmethod
    async def save_releases(db, releases):

        for r in releases:

            await ReleaseRepository.upsert_release(
                db=db,
                location_id=r["location_id"],
                title=r["title"],
                status=r["status"],
                description=r["description"],
                link=r["link"],
                image_url=r["image_url"]
            )