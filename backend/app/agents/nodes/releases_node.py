from backend.app.services.search_service import SearchService

async def releases_node(state):
    db = state["db"]
    query = state["rewritten_query"]

    results = await SearchService.hybrid_search(db, query, tables=["releases"])
    
    return {"context": results}
