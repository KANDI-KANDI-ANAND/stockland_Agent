from backend.app.repositories.location_repository import LocationRepository
from backend.app.repositories.home_repository import HomeRepository
from backend.app.repositories.news_repository import NewsRepository
from backend.app.repositories.ads_repository import AdsRepository


class ReportDataService:

    @staticmethod
    async def get_full_community_data(db, community_name):

        location = await LocationRepository.get_by_name(db, community_name)

        homes = await HomeRepository.get_by_location(db, community_name)

        news = await NewsRepository.get_by_location(db, community_name)

        ads = await AdsRepository.get_by_location(db, community_name)

        return {
            "location": location,
            "homes": homes,
            "news": news,
            "ads": ads
        }