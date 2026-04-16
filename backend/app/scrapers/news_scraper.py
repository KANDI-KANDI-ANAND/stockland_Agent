import asyncio


class NewsScraper:

    BASE_URL = "https://www.stockland.com.au/residential/news"

    def detect_location(self, link, locations):

        try:
            parts = link.split("/")

            if "residential" in parts:

                index = parts.index("residential")

                community_slug = parts[index + 2]

                community_slug = community_slug.replace("-", " ").lower()

                for loc in locations:

                    if loc.name.lower() in community_slug:
                        return loc.id

        except:
            pass

        return None


    async def load_all_news(self, page):

        print("Loading all news...")

        cards = page.locator("div.amenity-list-item-resource")

        while True:

            try:

                load_more = page.locator("text=Load more")

                if not await load_more.is_visible():
                    break

                previous_count = await cards.count()

                await load_more.click()

                # wait for next batch
                await asyncio.sleep(1)

                try:
                    await page.wait_for_function(
                        """(prev) => {
                            return document.querySelectorAll(
                                "div.amenity-list-item-resource"
                            ).length > prev
                        }""",
                        previous_count,
                        timeout=5000
                    )
                except:
                    pass

                new_count = await cards.count()

                print("Cards loaded:", new_count)

                if new_count == previous_count:
                    break

            except:
                break


    async def scrape_news_list(self, context, mode="full"):

        page = await context.new_page()

        print("Opening news page")

        await page.goto(self.BASE_URL, wait_until="domcontentloaded")

        await page.wait_for_timeout(3000)

        await self.load_all_news(page)

        cards_locator = page.locator("div.amenity-list-item-resource")

        count = await cards_locator.count()

        print("News cards found:", count)

        cards = await cards_locator.evaluate_all("""
        (cards) => {
            return cards.map(card => {

                const dateEl = card.querySelector("span.text-primary");
                const titleEl = card.querySelector("div.font-medium");
                const summaryEl = card.querySelector("div.line-clamp-3");
                const linkEl = card.querySelector("a[href*='/news-and-events/news/']");

                return {
                    published_date: dateEl ? dateEl.innerText.trim() : null,
                    title: titleEl ? titleEl.innerText.trim() : null,
                    summary: summaryEl ? summaryEl.innerText.trim() : null,
                    link: linkEl ? linkEl.getAttribute("href") : null
                };
            });
        }
        """)

        await page.close()

        news_items = []
        seen_links = set()

        for card in cards:

            link = card["link"]

            if not link:
                continue

            link = "https://www.stockland.com.au" + link

            if link in seen_links:
                continue

            seen_links.add(link)

            news_items.append({
                "title": card["title"],
                "summary": card["summary"],
                "content": card["summary"],
                "link": link,
                "published_date": card["published_date"]
            })

        print("News extracted:", len(news_items))

        return news_items