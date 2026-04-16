from sqlalchemy import select
from backend.app.database.models.news import News


async def news_node(state):

    db = state["db"]

    result = await db.execute(select(News).limit(5))

    news_list = result.scalars().all()

    items = []

    for n in news_list:

        items.append(n.title)

    state["answer"] = "\n".join(items)

    return state