import asyncio
from playwright.async_api import async_playwright

from backend.app.scrapers.news_scraper import NewsScraper
from backend.app.repositories.location_repository import LocationRepository
from backend.app.services.news_service import NewsService
from backend.app.database.connection import AsyncSessionLocal


async def main():

    scraper = NewsScraper()

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()

        async with AsyncSessionLocal() as db:

            locations = await LocationRepository.get_all_locations(db)

            articles = await scraper.scrape_news_list(context, mode="full")

            news_items = []

            for article in articles:

                location_id = scraper.detect_location(
                    article["link"],
                    locations
                )

                if not location_id:
                    continue

                news_items.append({
                    "location_id": location_id,
                    "title": article["title"],
                    "summary": article["summary"],
                    "content": article["summary"],
                    "link": article["link"],
                    "published_date": article["published_date"]
                })

            await NewsService.save_news(db, news_items)

            await db.commit()

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())