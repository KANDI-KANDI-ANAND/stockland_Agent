from backend.app.repositories.location_repository import LocationRepository
from backend.app.services.query_embedding_service import QueryEmbeddingService
from backend.app.core.llm_client import LLMClient


class LocationService:

    @staticmethod
    async def search_locations(db, question):

        embedding = await QueryEmbeddingService.embed_query(question)

        results = await LocationRepository.semantic_search(
            db,
            embedding
        )

        prompt = "\n".join([
            f"Name: {r['name']}\nDescription: {r['description']}\nAmenities: {', '.join(r['amenities'])}"
            for r in results
        ])

        answer = await LLMClient.generate_answer(prompt)

        return {
            "answer": answer,
            "locations": results
        }