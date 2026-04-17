import asyncio
from sqlalchemy import text

from backend.app.services.embedding_service import EmbeddingService

class SearchService:

    VECTOR_LIMIT = 10
    KEYWORD_LIMIT = 10
    FINAL_LIMIT = 15
    MIN_SCORE = 0.0


    # -----------------------------
    # VECTOR SEARCH
    # -----------------------------
    @staticmethod
    async def vector_search(db, query_embedding, tables):

        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        sql = text("""
        (SELECT 'location' as type, id, name as title, summary,
            1 - (embedding <=> CAST(:embedding AS vector)) as score
        FROM locations
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit)
        UNION ALL
        (SELECT 'home' as type, id, home_type as title, summary,
            1 - (embedding <=> CAST(:embedding AS vector)) as score
        FROM homes
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit)
        UNION ALL
        (SELECT 'news' as type, id, title, summary,
            1 - (embedding <=> CAST(:embedding AS vector)) as score
        FROM news
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit)
        UNION ALL
        (SELECT 'ads' as type, id, ad_text as title, summary,
            1 - (embedding <=> CAST(:embedding AS vector)) as score
        FROM ads
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit)
        UNION ALL
        (SELECT 'release' as type, id, title, summary,
            1 - (embedding <=> CAST(:embedding AS vector)) as score
        FROM releases
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit)
        """)
        result = await db.execute(
            sql,
            {"embedding": embedding_str, "limit": SearchService.VECTOR_LIMIT}
        )

        rows = result.fetchall()

        return [
            {
                "type": r.type,
                "id": r.id,
                "title": r.title,
                "summary": r.summary,
                "score": float(r.score),
                "source": "vector"
            }
            for r in rows
        ]


    # -----------------------------
    # KEYWORD SEARCH
    # -----------------------------
    @staticmethod
    async def keyword_search(db, query, tables=None):

        sql = text("""
        (SELECT 'location' as type, id, name as title, summary,
            ts_rank(to_tsvector(summary), plainto_tsquery(:query)) as score
        FROM locations
        WHERE to_tsvector(summary) @@ plainto_tsquery(:query)
        LIMIT :limit)

        UNION ALL

        (SELECT 'home' as type, id, home_type as title, summary,
            ts_rank(to_tsvector(summary), plainto_tsquery(:query)) as score
        FROM homes
        WHERE to_tsvector(summary) @@ plainto_tsquery(:query)
        LIMIT :limit)

        UNION ALL

        (SELECT 'news' as type, id, title, summary,
            ts_rank(to_tsvector(summary), plainto_tsquery(:query)) as score
        FROM news
        WHERE to_tsvector(summary) @@ plainto_tsquery(:query)
        LIMIT :limit)

        UNION ALL

        (SELECT 'ads' as type, id, ad_text as title, summary,
            ts_rank(to_tsvector(summary), plainto_tsquery(:query)) as score
        FROM ads
        WHERE to_tsvector(summary) @@ plainto_tsquery(:query)
        LIMIT :limit)

        UNION ALL

        (SELECT 'release' as type, id, title, summary,
            ts_rank(to_tsvector(summary), plainto_tsquery(:query)) as score
        FROM releases
        WHERE to_tsvector(summary) @@ plainto_tsquery(:query)
        LIMIT :limit)
        """)

        result = await db.execute(
            sql,
            {
                "query": query,
                "limit": SearchService.KEYWORD_LIMIT
            }
        )

        rows = result.fetchall()

        return [
            {
                "type": r.type,
                "id": r.id,
                "title": r.title,
                "summary": r.summary,
                "score": float(r.score),
                "source": "keyword"
            }
            for r in rows
        ]


    # -----------------------------
    # HYBRID SEARCH
    # -----------------------------
    @staticmethod
    async def hybrid_search(db, query, tables=None):

        if tables is None:
            tables = ["locations", "homes", "news", "ads", "releases"]

        query_embedding = EmbeddingService.generate_embedding(query)

        vector_results = await SearchService.vector_search(db, query_embedding, tables)

        keyword_results = await SearchService.keyword_search(db, query, tables)

        combined = vector_results + keyword_results

        filtered = [
            r for r in combined
            if r["score"] >= SearchService.MIN_SCORE
        ]

        # Remove duplicates
        seen = set()
        unique_results = []

        for r in filtered:
            key = (r["type"], r["id"])

            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        # Rank results
        ranked = sorted(
            unique_results,
            key=lambda x: x["score"],
            reverse=True
        )

        print(f"🔍 SEARCH DEBUG: Found {len(ranked)} results for query: '{query}'")
        
        return ranked[:SearchService.FINAL_LIMIT]

        

