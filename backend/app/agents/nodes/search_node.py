from backend.app.services.search_service import SearchService

async def search_node(state):

    db = state["db"]
    query = state["rewritten_query"]

    results = await SearchService.hybrid_search(db, query)

    state["context"] = results

    return state