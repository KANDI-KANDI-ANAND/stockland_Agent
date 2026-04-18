import asyncio

class AdsScraper:

    ADS_URLS = [
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=159758724052194",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=341899012565298",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=580854591981233",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=167279036669721",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=134591239921256",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=1446767475618588",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=1395890630676566",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=340985179291234",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=156030774420364",
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=350424078436623"
    ]


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

        all_ads = [] 

        for url in self.ADS_URLS:
            page = await context.new_page()
            print(f"Opening Ads Library for: {url}...")
            try:
                await page.goto(url, wait_until="domcontentloaded")
                await page.wait_for_timeout(8000)
                await self.scroll_page(page)
                start_labels = page.locator("text=Started running on")
                count = await start_labels.count()
                print(f"Ads detected for this URL: {count}")

                for i in range(count):

                    label = start_labels.nth(i)

                    card = label.locator("xpath=ancestor::div[5]")

                    text = await card.inner_text()

                    start_date = None

                    for line in text.split("\n"):

                        if "Started running on" in line:

                            start_date = line.replace(
                                "Started running on",
                                ""
                            ).strip()

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

                    image_url = None

                    img = card.locator("img")

                    if await img.count() > 0:

                        image_url = await img.first.get_attribute("src")

                    destination = None

                    links = card.locator("a")

                    link_count = await links.count()

                    for j in range(link_count):

                        link = links.nth(j)

                        href = await link.get_attribute("href")

                        if href and "stockland.com.au" in href:

                            destination = href
                            break

                    all_ads.append({
                        "ad_text": ad_text,
                        "image_url": image_url,
                        "start_date": start_date,
                        "destination": destination
                    })
            except Exception as e:
                print(f"Error scraping {url}: {e}")
            finally:
                await page.close() 
            
            await asyncio.sleep(5)

        return all_ads
