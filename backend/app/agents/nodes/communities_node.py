from backend.app.repositories.location_repository import LocationRepository
from backend.app.services.embedding_service import EmbeddingService

async def communities_node(state):

    db = state["db"]
    query = state["rewritten_query"]

    embedding = EmbeddingService.generate_embedding(query)

    results = await LocationRepository.semantic_search(db, embedding)

    state["context"] = results

    return state