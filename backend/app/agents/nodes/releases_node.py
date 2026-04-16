from sqlalchemy import select
from backend.app.database.models.release import Release


async def releases_node(state):

    db = state["db"]

    result = await db.execute(select(Release).limit(5))

    releases = result.scalars().all()

    items = []

    for r in releases:

        items.append(r.title)

    state["answer"] = "\n".join(items)

    return state