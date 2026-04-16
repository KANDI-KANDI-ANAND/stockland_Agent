from backend.app.repositories.interest_repository import InterestRepository


class InterestService:

    @staticmethod
    async def save_interest(db, data):

        return await InterestRepository.create_interest(db, data)