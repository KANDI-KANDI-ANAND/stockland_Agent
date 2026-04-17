from backend.app.services.search_service import SearchService

async def homes_node(state):
    db = state["db"]
    
    query = state.get("rewritten_query") or state.get("question")

    results = await SearchService.hybrid_search(db, query)
    
    state["context"] = results
    
    return state
