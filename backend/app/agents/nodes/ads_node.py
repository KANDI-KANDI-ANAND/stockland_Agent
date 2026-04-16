from sqlalchemy import select
from backend.app.database.models.ads import Ad


async def ads_node(state):

    db = state["db"]

    result = await db.execute(select(Ad))

    ads = result.scalars().all()

    items = []

    for ad in ads:

        items.append(ad.ad_text)

    state["answer"] = "\n".join(items)

    return state