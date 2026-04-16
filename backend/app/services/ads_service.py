from backend.app.repositories.ads_repository import AdsRepository
from urllib.parse import urlparse


class AdsService:

    @staticmethod
    async def save_ads(db, ads, locations):

        for ad in ads:

            location_id = None

            if ad["destination"]:

                parsed = urlparse(ad["destination"])

                slug = parsed.path.strip("/").split("/")[-1]

                slug = slug.replace("-", " ").lower()

                for loc in locations:

                    if loc.name.lower() in slug:

                        location_id = loc.id
                        break

            if not location_id:
                print("Location not detected, storing ad without location")

            await AdsRepository.upsert_ad(
                db=db,
                location_id=location_id,
                ad_text=ad["ad_text"],
                image_url=ad["image_url"],
                start_date=ad["start_date"]
            )

            print(ad)

    