import asyncio
from playwright.async_api import async_playwright

from backend.app.scrapers.release_scraper import ReleaseScraper
from backend.app.services.release_service import ReleaseService
from backend.app.database.connection import AsyncSessionLocal
from backend.app.repositories.location_repository import LocationRepository


async def main():

    scraper = ReleaseScraper()

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()

        async with AsyncSessionLocal() as db:

            locations = await LocationRepository.get_all_locations(db)

            # Aura is the location for these updates
            aura = next(l for l in locations if l.name.lower() == "aura")

            releases = await scraper.scrape_releases(context, aura.id)

            await ReleaseService.save_releases(db, releases)

            await db.commit()

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())