import hashlib
from backend.app.agents.memory.conversation_memory import ConversationMemory
from backend.app.agents.agent_graph_builder import build_graph
from backend.app.core.redis_cache import redis_client

graph = build_graph()


class StocklandAgent:

    @staticmethod
    async def run(db, question, session_id='default'):

        question_hash = hashlib.md5(question.lower().strip().encode()).hexdigest()

        cache_key = f"answer_cache:{question_hash}"

        # 2. CHECK CACHE: See if we answered this before
        cached_answer = redis_client.get_cache(cache_key)

        if cached_answer:

            print(f"--- CACHE HIT: Returning stored answer for '{question}' ---")

            # We still add it to the user's specific history so they stay in context
            memory = ConversationMemory(session_id)
            memory.add_message("user", question)
            memory.add_message("assistant", cached_answer)
            return {"answer": cached_answer}

        # 3. NO CACHE: Run the full AI process

        print(f"--- CACHE MISS: Running AI for '{question}' ---")

        memory = ConversationMemory(session_id)

        memory.add_message("user", question)

        state = {
            "question": question,
            "history": memory.get_history(),
            "rewritten_query": question,
            "db": db,
            "lead": {}
        }
        result = await graph.ainvoke(state)
        final_answer = result["answer"]

        # 4. SAVE TO CACHE: Store the new answer for next time
        negative_phrases = ["can't find", "no information", "no specific details", "couldn't find"]
        is_negative = any(phrase in final_answer.lower() for phrase in negative_phrases)
        if not is_negative:
            redis_client.set_cache(cache_key, final_answer)
            print("💾 Result cached (Positive answer)")
        else:
            print("🛑 Negative response detected - Skipping cache to allow for future database updates.")
        memory.add_message("assistant", final_answer)
        return result