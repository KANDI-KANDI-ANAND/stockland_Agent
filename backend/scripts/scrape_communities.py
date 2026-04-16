import asyncio

from backend.app.scrapers.community_scraper import CommunityScraper
from backend.app.services.community_service import CommunityService
from backend.app.database.connection import AsyncSessionLocal


async def main():

    scraper = CommunityScraper()
    
    communities = await scraper.scrape_all()

    async with AsyncSessionLocal() as db:

        await CommunityService.save_communities(db, communities)

        await db.commit()

    print("Communities saved successfully")


if __name__ == "__main__":
    asyncio.run(main())