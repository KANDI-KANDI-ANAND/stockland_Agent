from backend.app.agents.memory.conversation_memory import ConversationMemory
from backend.app.agents.agent_graph_builder import build_graph
from backend.app.services.embedding_service import EmbeddingService
from backend.app.repositories.semantic_cache_repository import SemanticCacheRepository

graph = build_graph()

class StocklandAgent:

    @staticmethod
    async def run(db, question, session_id='default'):
        
        question_embedding = EmbeddingService.generate_embedding(question)
        cached_match = await SemanticCacheRepository.get_closest_match(db, question_embedding)

        if cached_match:
            print(f"--- SEMANTIC CACHE HIT ({round(cached_match['similarity'] * 100)}%) ---")
            print(f"Match found for: '{cached_match['question']}'")
            
            memory = ConversationMemory(session_id)
            memory.add_message("user", question)
            memory.add_message("assistant", cached_match["answer"])
            
            return {"answer": cached_match["answer"]}

        print(f"--- CACHE MISS: Running AI for '{question}' ---")

        memory = ConversationMemory(session_id)
        memory.add_message("user", question)

        state = {
            "question": question,
            "history": memory.get_history(),
            "rewritten_query": question,
            "db": db,
            "context": [],
            "intent": [],
            "lead": {}
        }

        result = await graph.ainvoke(state)
        final_answer = result["answer"]
        negative_phrases = ["can't find", "no information", "no specific details", "couldn't find"]
        is_negative = any(phrase in final_answer.lower() for phrase in negative_phrases)

        if not is_negative:
            await SemanticCacheRepository.save_cache(
                db, 
                result.get("rewritten_query"), 
                final_answer, 
                question_embedding
            )
            print("Successfully cached positive answer in Postgres.")
        else:
            print("Negative response detected - skipping semantic cache.")

        memory.add_message("assistant", final_answer)
        return result
