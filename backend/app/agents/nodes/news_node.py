from backend.app.services.search_service import SearchService

async def news_node(state):
    db = state["db"]
    query = state["rewritten_query"]

    results = await SearchService.hybrid_search(db, query, tables=["news"])
    
    return {"context": results}
