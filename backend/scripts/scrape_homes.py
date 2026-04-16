import asyncio
from playwright.async_api import async_playwright

from backend.app.scrapers.homes_scraper import HomeScraper
from backend.app.services.home_service import HomeService
from backend.app.database.connection import AsyncSessionLocal
from backend.app.repositories.location_repository import LocationRepository


async def main():

    scraper = HomeScraper()

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()

        async with AsyncSessionLocal() as db:

            locations = await LocationRepository.get_all_locations(db)

            for location in locations:

                homes = await scraper.scrape_homes(
                    context,
                    location.url,
                    location.id
                )

                await HomeService.save_homes(db, homes)

                await db.commit()

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())