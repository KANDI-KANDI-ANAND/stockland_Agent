import asyncio

class AdsScraper:

    ADS_URL = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&search_type=page&view_all_page_id=159758724052194"


    async def scroll_page(self, page):

        previous_height = None

        while True:

            current_height = await page.evaluate("document.body.scrollHeight")

            if previous_height == current_height:
                break

            previous_height = current_height

            await page.evaluate(
                "window.scrollTo(0, document.body.scrollHeight)"
            )

            await asyncio.sleep(2)


    async def scrape_ads(self, context):

        page = await context.new_page()

        print("Opening Ads Library...")

        await page.goto(self.ADS_URL, wait_until="domcontentloaded")

        # give time for JS to load ads
        await page.wait_for_timeout(8000)

        await self.scroll_page(page)

        # anchor on stable text
        start_labels = page.locator("text=Started running on")

        count = await start_labels.count()

        print("Ads detected:", count)

        ads = []

        for i in range(count):

            label = start_labels.nth(i)

        # move up DOM to reach card container
            card = label.locator("xpath=ancestor::div[5]")

            text = await card.inner_text()

        # -----------------------
        # Extract start date
        # -----------------------

            start_date = None

            for line in text.split("\n"):

                if "Started running on" in line:

                    start_date = line.replace(
                        "Started running on",
                        ""
                    ).strip()

        # -----------------------
        # Extract ad text
        # -----------------------

            ad_text = None

            spans = card.locator("span")

            span_count = await spans.count()

            for j in range(span_count):

                span = spans.nth(j)

                try:

                    content = (await span.inner_text()).strip()

                    if len(content) > 40 and "Sponsored" not in content:

                        ad_text = content
                        break

                except:
                    pass

        # -----------------------
        # Extract image
        # -----------------------

            image_url = None

            img = card.locator("img")

            if await img.count() > 0:

                image_url = await img.first.get_attribute("src")

        # -----------------------
        # Extract destination link
        # -----------------------

            destination = None

            links = card.locator("a")

            link_count = await links.count()

            for j in range(link_count):

                link = links.nth(j)

                href = await link.get_attribute("href")

                if href and "stockland.com.au" in href:

                    destination = href
                    break

            ads.append({
                "ad_text": ad_text,
                "image_url": image_url,
                "start_date": start_date,
                "destination": destination
            })

        await page.close()

        return ads
