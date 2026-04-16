import asyncio
from playwright.async_api import async_playwright

from backend.app.scrapers.ads_scraper import AdsScraper
from backend.app.services.ads_service import AdsService
from backend.app.database.connection import AsyncSessionLocal
from backend.app.repositories.location_repository import LocationRepository


async def main():

    scraper = AdsScraper()

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()

        async with AsyncSessionLocal() as db:

            locations = await LocationRepository.get_all_locations(db)

            ads = await scraper.scrape_ads(context)

            await AdsService.save_ads(db, ads, locations)

            await db.commit()

        await browser.close()


if __name__ == "__main__":

    asyncio.run(main())