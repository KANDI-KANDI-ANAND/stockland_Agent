from sqlalchemy import text
from backend.app.database.models.semantic_cache import SemanticCache

class SemanticCacheRepository:

    @staticmethod
    async def get_closest_match(db, embedding, threshold=0.96):
        embedding_str = "[" + ",".join(map(str, embedding)) + "]"
        
        query = text("""
            SELECT question, answer, 1 - (embedding <=> CAST(:embedding AS vector)) as similarity
            FROM semantic_cache
            WHERE 1 - (embedding <=> CAST(:embedding AS vector)) > :threshold
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT 1
        """)

        result = await db.execute(query, {"embedding": embedding_str, "threshold": threshold})
        return result.mappings().first()

    @staticmethod
    async def save_cache(db, question, answer, embedding):
        new_entry = SemanticCache(
            question=question,
            answer=answer,
            embedding=embedding
        )
        db.add(new_entry)
        await db.commit()
