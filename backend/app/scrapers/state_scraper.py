import asyncio
from playwright.async_api import async_playwright


STATE_URLS = [
    "https://www.stockland.com.au/residential/qld",
    "https://www.stockland.com.au/residential/nsw",
    "https://www.stockland.com.au/residential/vic",
    "https://www.stockland.com.au/residential/wa"
]


class StateCommunitiesScraper:

    async def scrape_state(self, page, state_url: str):

        print(f"\nScraping state page: {state_url}")

        await page.goto(state_url)

        await page.wait_for_timeout(4000)

        links = await page.locator("a").all()

        print("Total links found:", len(links))

        community_links = []

        for link in links:

            href = await link.get_attribute("href")

            if not href:
                continue

            if not href.startswith("/residential/"):
                continue
            if "/find-your-home" in href or "/news" in href:
                continue

            parts = href.strip("/").split("/")

            if len(parts) == 3:

                state = parts[1]

                valid_states = ["qld", "nsw", "vic", "wa"]

                if state in valid_states:

                    url = f"https://www.stockland.com.au{href}"

                    community_links.append(url)

        community_links = list(set(community_links))

        print("Communities found:", len(community_links))

        for url in community_links:
            print(url)

        return community_links


    async def scrape_all_states(self):

        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=False)

            page = await browser.new_page()

            all_links = []

            for state_url in STATE_URLS:

                links = await self.scrape_state(page, state_url)

                all_links.extend(links)

            await browser.close()

            return list(set(all_links))


async def main():

    scraper = StateCommunitiesScraper()

    communities = await scraper.scrape_all_states()

    print("\nFinal Communities List:", len(communities))


if __name__ == "__main__":

    asyncio.run(main())