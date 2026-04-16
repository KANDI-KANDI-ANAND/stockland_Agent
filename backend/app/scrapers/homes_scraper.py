import asyncio
from playwright.async_api import async_playwright


class HomeScraper:

    async def scrape_page(self, page, location_id):

        homes = []

        titles = await page.query_selector_all("h3.text-brand-xl")

        for title_el in titles:

            card = await title_el.evaluate_handle(
                "el => el.closest('div.flex.flex-col')"
            )

            title = await title_el.inner_text()

            # -------------------------
            # Home type
            # -------------------------

            home_category = "House & Land"

            title_lower = title.lower()

            if "indicative" in title_lower:
                home_category = "Indicative House & Land"

            if "lot" in title_lower:
                home_category = "Land"

            home_type = f"{home_category} - {title}"

            # -------------------------
            # Price
            # -------------------------

            price = None

            price_el = await card.query_selector("text=/\\$/")

            if price_el:

                price_text = await price_el.inner_text()

                price = (
                    price_text
                    .replace("From $", "")
                    .replace("$", "")
                    .replace(",", "")
                    .replace("*", "")
                    .strip()
                )

                try:
                    price = float(price)
                except:
                    price = None

            # -------------------------
            # Bedrooms / Bathrooms
            # -------------------------

            bedrooms = None
            bathrooms = None

            spans = await card.query_selector_all("span.text-brand-md")

            numbers = []

            for span in spans:

                text = (await span.inner_text()).strip()

                if text.isdigit():
                    numbers.append(int(text))

            if len(numbers) >= 1:
                bedrooms = numbers[0]

            if len(numbers) >= 2:
                bathrooms = numbers[1]

            # -------------------------
            # Size
            # -------------------------

            size = None

            for span in spans:

                text = (await span.inner_text()).strip()

                if "m" in text:

                    sup = await span.query_selector("sup")

                    if sup:

                        sup_text = await sup.inner_text()

                        if sup_text == "2":

                            try:
                                size = float(text.replace("m", "").strip())
                            except:
                                pass

            # -------------------------
            # Image
            # -------------------------

            image_url = None

            img = await card.query_selector("picture img")

            if img:

                image_url = await img.get_attribute("src")

                if not image_url:
                    image_url = await img.get_attribute("data-src")

                if not image_url:

                    srcset = await img.get_attribute("srcset")

                    if srcset:
                        image_url = srcset.split(" ")[0]

            homes.append({
                "location_id": location_id,
                "home_type": home_type,
                "price": price,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "size": size,
                "image_url": image_url
            })

        return homes


    async def scrape_homes(self, context, community_url, location_id):

        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=False)

            context = await browser.new_context()

            page = await context.new_page()

            url = community_url + "/find-your-home"

            print("\nScraping:", url)

            await page.goto(url, timeout=60000)

            await page.wait_for_timeout(4000)

            all_homes = []

            buttons = await page.query_selector_all("button.text-brand-sm")

            total_pages = len(buttons) if buttons else 1

            for page_number in range(total_pages):

                print("Page:", page_number + 1)

                if page_number > 0:

                    buttons = await page.query_selector_all("button.text-brand-sm")

                    await buttons[page_number].click()

                    await page.wait_for_timeout(3000)

                homes = await self.scrape_page(page, location_id)

                all_homes.extend(homes)

            await browser.close()

            return all_homes