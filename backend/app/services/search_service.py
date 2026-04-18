import asyncio
import json
from sqlalchemy import text

from backend.app.services.embedding_service import EmbeddingService
from backend.app.core.llm_client import LLMClient

class SearchService:

    VECTOR_LIMIT = 20
    KEYWORD_LIMIT = 20
    FINAL_LIMIT = 25

    @staticmethod
    async def _extract_filters(query: str):
        prompt = f"""
        Analyze the search query and extract property filters in JSON format.
        
        QUERY: "{query}"
        
        JSON STRUCTURE:
        {{
            "location": string or null,
            "max_price": number or null,
            "min_price": number or null,
            "min_bedrooms": number or null,
            "min_bathrooms": number or null,
            "min_area": number or null,
            "max_area": number or null,
            "property_type": string or null
        }}
        
        RULES:
        - If the user says "under 500k", max_price is 500000.
        - If they mention a place (Aura, Highlands, etc.), put it in "location".
        - Only extract if the user is being specific.
        - Return ONLY the JSON block.
        """
        try:
            response = await LLMClient.generate_answer(prompt)
            
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return None


    @staticmethod
    async def _structured_home_search(db, filters):
        conditions = ["1=1"]
        params = {}
        if filters.get("max_price"):
            conditions.append("h.price <= :max_price")
            params["max_price"] = filters["max_price"]
        if filters.get("min_price"):
            conditions.append("h.price >= :min_price")
            params["min_price"] = filters["min_price"]
        if filters.get("min_bedrooms"):
            conditions.append("h.bedrooms >= :min_bedrooms")
            params["min_bedrooms"] = filters["min_bedrooms"]
        if filters.get("min_bathrooms"):
            conditions.append("h.bathrooms >= :min_bathrooms")
            params["min_bathrooms"] = filters["min_bathrooms"]
        if filters.get("min_area"):
            conditions.append("h.size >= :min_area")
            params["min_area"] = filters["min_area"]
        if filters.get("max_area"):
            conditions.append("h.size <= :max_area")
            params["max_area"] = filters["max_area"]
        if filters.get("property_type"):
            conditions.append("LOWER(h.home_type) LIKE LOWER(:property_type)")
            params["property_type"] = f"%{filters['property_type']}%"
        if filters.get("location"):
            conditions.append("LOWER(l.name) LIKE LOWER(:loc)")
            params["loc"] = f"%{filters['location']}%"
        sql = text(f"""
            SELECT 'home' as type, h.id, h.home_type as title, 
                   (h.summary || ' | Land Area: ' || h.size || 'm²') as summary,
                   h.image_url, 1.0 as score -- Added image_url
            FROM homes h
            JOIN locations l ON h.location_id = l.id
            WHERE {" AND ".join(conditions)}
            ORDER BY h.price ASC
            LIMIT 30
        """)
        
        result = await db.execute(sql, params)
        rows = result.fetchall()
        return [{"type": r.type, "id": r.id, "title": r.title, "summary": r.summary, "image_url": getattr(r, "image_url", None), "score": float(r.score), "source": "strict"} for r in rows]   


    # -----------------------------
    # VECTOR SEARCH
    # -----------------------------
    @staticmethod
    async def vector_search(db, query_embedding, tables):

        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        sql = text("""
        (SELECT 'location' as type, id, name as title, summary, 
            (1 - (embedding <=> CAST(:embedding AS vector))) * 1.1 as score 
         FROM locations ORDER BY score DESC LIMIT 15)
        UNION ALL
        (SELECT 'home' as type, id, home_type as title, 
            (summary || ' | Land Area: ' || size || 'm²') as summary, 
            image_url, -- Added image_url
            (1 - (embedding <=> CAST(:embedding AS vector))) * 1.2 as score 
         FROM homes ORDER BY score DESC LIMIT 25)
        UNION ALL
        (SELECT 'news' as type, id, title, summary, 
            (1 - (embedding <=> CAST(:embedding AS vector))) as score 
         FROM news ORDER BY score DESC LIMIT 10)
        UNION ALL
        (SELECT 'ads' as type, id, ad_text as title, summary, 
            image_url, -- Added image_url
            (1 - (embedding <=> CAST(:embedding AS vector))) as score 
         FROM ads ORDER BY score DESC LIMIT 10)
        UNION ALL
        (SELECT 'release' as type, id, title, summary,
            (1 - (embedding <=> CAST(:embedding AS vector))) as score
        FROM releases ORDER BY score DESC LIMIT 10)
        """)
        result = await db.execute(
            sql,
            {"embedding": embedding_str}
        )

        rows = result.fetchall()

        return [
            {
                "type": r.type,
                "id": r.id,
                "title": r.title,
                "summary": r.summary,
                "image_url": getattr(r, "image_url", None),
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
            CASE WHEN name ILIKE :q_like THEN 1.0 ELSE ts_rank(to_tsvector(summary), plainto_tsquery(:q)) END as score
         FROM locations WHERE to_tsvector(summary) @@ plainto_tsquery(:q) OR name ILIKE :q_like LIMIT 10)
        UNION ALL
        (SELECT 'home' as type, id, home_type as title, 
            (summary || ' | Land Area: ' || size || 'm²') as summary, 
            image_url, -- Added image_url
            CASE WHEN home_type ILIKE :q_like THEN 1.0 ELSE ts_rank(to_tsvector(summary), plainto_tsquery(:q)) END as score
         FROM homes WHERE to_tsvector(summary) @@ plainto_tsquery(:q) OR home_type ILIKE :q_like LIMIT 15)
        UNION ALL
        (SELECT 'news' as type, id, title, summary, 
            ts_rank(to_tsvector(summary), plainto_tsquery(:q)) as score
         FROM news WHERE to_tsvector(summary) @@ plainto_tsquery(:q) LIMIT 10)
        UNION ALL
        (SELECT 'ads' as type, id, ad_text as title, summary, 
            image_url, -- Added image_url
            ts_rank(to_tsvector(ad_text), plainto_tsquery(:q)) as score
         FROM ads WHERE to_tsvector(ad_text) @@ plainto_tsquery(:q) LIMIT 10)
        UNION ALL
        (SELECT 'release' as type, id, title, summary, 
            ts_rank(to_tsvector(summary), plainto_tsquery(:q)) as score
         FROM releases WHERE to_tsvector(summary) @@ plainto_tsquery(:q) LIMIT 10)
        """)

        result = await db.execute(
            sql,
            {
                "q": query,
                "q_like": f"%{query}%"
            }
        )

        rows = result.fetchall()

        return [
            {
                "type": r.type,
                "id": r.id,
                "title": r.title,
                "summary": r.summary,
                "image_url": getattr(r, "image_url", None),
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
        filters = await SearchService._extract_filters(query)

        strict_results = []

        if filters and any(v is not None for v in filters.values()):
            print(f"--- STRICT SEARCH ACTIVATED: {filters} ---")
            strict_results = await SearchService._structured_home_search(db, filters)
        
        query_embedding = EmbeddingService.generate_embedding(query)
        
        vector_results = await SearchService.vector_search(db, query_embedding, tables)
        
        keyword_results = await SearchService.keyword_search(db, query, tables)
        
        combined = strict_results + vector_results + keyword_results
        
        seen = set()
        unique_results = []
        
        for r in combined:
            key = (r["type"], r["id"])
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        ranked = sorted(
            unique_results,
            key=lambda x: (x["source"] == "strict", x["score"]),
            reverse=True
        )
        
        print(f"🔍 SEARCH DEBUG: Final set contains {len(ranked)} results.")
        return ranked[:SearchService.FINAL_LIMIT]

        

