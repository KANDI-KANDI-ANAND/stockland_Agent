from backend.app.services.chat_service import ChatService
from backend.app.services.search_service import SearchService

class AgentTools:

    @staticmethod
    async def search_stockland_data(db, query):

        results = await SearchService.hybrid_search(
            db,
            query,
            limit=10
        )

        return results