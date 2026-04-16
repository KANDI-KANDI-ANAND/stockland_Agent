from backend.app.core.reranker_model import reranker


class RerankerService:

    @staticmethod
    def rerank(query: str, documents: list, top_k: int = 10):

        pairs = []

        for doc in documents:
            pairs.append((query, doc["summary"]))

        scores = reranker.predict(pairs)

        for i, score in enumerate(scores):
            documents[i]["rerank_score"] = float(score)

        documents.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return documents[:top_k]