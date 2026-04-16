from sqlalchemy import select
from backend.app.database.models.home import Home


async def homes_node(state):

    db = state["db"]

    result = await db.execute(select(Home))

    homes = result.scalars().all()

    data = []

    for h in homes:
        data.append(
            f"{h.home_type} - {h.bedrooms} bedrooms - ${h.price}"
        )

    state["answer"] = "\n".join(data)

    return state