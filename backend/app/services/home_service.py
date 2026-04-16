from backend.app.repositories.home_repository import HomeRepository


class HomeService:

    @staticmethod
    async def save_homes(db, homes):

        for home in homes:

            await HomeRepository.upsert_home(
                db=db,
                **home
            )