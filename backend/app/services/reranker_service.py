from backend.app.core.reranker_model import reranker


class RerankerService:

    @staticmethod
    def rerank(query: str, documents: list, top_k: int = 10):

        return documents[:top_k]