import asyncio


class ReleaseScraper:

    URL = "https://www.stockland.com.au/residential/qld/aura/life-at-aura/construction-updates"


    async def scroll_page(self, page):

        previous_height = None

        while True:

            current_height = await page.evaluate("document.body.scrollHeight")

            if previous_height == current_height:
                break

            previous_height = current_height

            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            await asyncio.sleep(2)


    async def scrape_releases(self, context, location_id):

        page = await context.new_page()

        print("Opening construction updates page")

        await page.goto(self.URL, wait_until="domcontentloaded")

        await page.wait_for_timeout(4000)

        await self.scroll_page(page)

        cards = page.locator("div.standard-card")

        count = await cards.count()

        print("Release cards found:", count)

        releases = []

        for i in range(count):

            card = cards.nth(i)

            # status
            status = None
            status_el = card.locator("div.flex.items-center")

            if await status_el.count() > 0:
                status = (await status_el.first.inner_text()).strip()

            # title
            title = None
            title_el = card.locator("div.promo-card-heading")

            if await title_el.count() > 0:
                title = (await title_el.first.inner_text()).strip()

            # description
            description = None
            desc_el = card.locator("div.grow.text-brand-base")

            if await desc_el.count() > 0:
                description = (await desc_el.first.inner_text()).strip()

            # link
            link = None
            link_el = card.locator("a[aria-label='Find out more']")

            if await link_el.count() > 0:
                href = await link_el.first.get_attribute("href")

                if href:
                    link = "https://www.stockland.com.au" + href

            # image
            image_url = None
            img = card.locator("picture img")

            if await img.count() > 0:
                image_url = await img.first.get_attribute("src")

            releases.append({
                "location_id": location_id,
                "title": title,
                "status": status,
                "description": description,
                "link": link,
                "image_url": image_url
            })

        await page.close()

        return releases