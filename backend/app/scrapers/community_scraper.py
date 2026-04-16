import asyncio
from playwright.async_api import async_playwright
from backend.app.scrapers.state_scraper import StateCommunitiesScraper


class CommunityScraper:

    def clean_community_name(self, name: str):

        name = name.lower().strip()

        prefixes = [
            "discover ",
            "explore ",
            "welcome to ",
            "live at ",
            "life at "
        ]

        for prefix in prefixes:
            if name.startswith(prefix):
                name = name.replace(prefix, "")

        return name.title().strip()


    async def scroll_page(self, page):

        previous_height = None

        while True:

            current_height = await page.evaluate("document.body.scrollHeight")

            if previous_height == current_height:
                break

            previous_height = current_height

            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            await asyncio.sleep(1)


    async def extract_amenities(self, page):

        amenities = set()

        spans = page.locator("span")
        count = await spans.count()

        for i in range(count):

            try:
                text = (await spans.nth(i).inner_text()).strip()

                if len(text) < 3 or len(text) > 40:
                    continue

                if text.isdigit():
                    continue

                if any(x in text.lower() for x in [
                    "promotion","finish","offer","privacy","contact","explore","discover","terms"
                ]):
                    continue

                if any(x in text.lower() for x in [
                    "education","school","medical","hospital","park",
                    "transport","retail","shopping","dining","leisure",
                    "pool","walkway","sports","childcare"
                ]):
                    amenities.add(text)

            except:
                pass

        return list(amenities)


    async def scrape_community(self, page, community_url):

        print(f"\nScraping community: {community_url}")

        await page.goto(community_url, wait_until="domcontentloaded", timeout=60000)

        await page.wait_for_timeout(2000)

        await self.scroll_page(page)

        await page.wait_for_selector("h1", timeout=20000)

        hero = page.locator("h1").first

        name = await hero.inner_text()

        name = self.clean_community_name(name)

        container = hero.locator("xpath=..")

        text = await container.inner_text()

        lines = text.split("\n")

        description_parts = []

        for line in lines:

            line = line.strip()

            if len(line) < 30:
                continue

            if any(x in line for x in ["Privacy", "Enquire", "Explore", "Contact"]):
                continue

            description_parts.append(line)

        description = " ".join(description_parts[:3]).strip()

        amenities = await self.extract_amenities(page)

        return {
            "name": name,
            "description": description,
            "amenities": amenities,
            "url": community_url
        }


    async def scrape_all(self):

        communities = []

        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=False)

            context = await browser.new_context()

            state_scraper = StateCommunitiesScraper()

            community_urls = await state_scraper.scrape_all_states()

            print("\nTotal communities discovered:", len(community_urls))

            for url in community_urls:

                try:

                    page = await context.new_page()

                    data = await self.scrape_community(page, url)

                    state = url.split("/")[4].upper()

                    data["state"] = state

                    communities.append(data)

                    await page.close()

                    await asyncio.sleep(1)

                except Exception as e:

                    print("Error scraping:", url, e)

            await browser.close()

        return communities