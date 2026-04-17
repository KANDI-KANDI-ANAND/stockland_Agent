from backend.app.core.llm_client import LLMClient


async def query_rewrite_node(state):

    question = state["question"]
    history = state.get("history", [])

    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history[-3:]])

    prompt = f"""
Given the history and message, output a clean, standalone search query using only KEYWORDS.
DO NOT use sentences. DO NOT use quotes.
HISTORY: {history_text}
USER MESSAGE: {question}
Rewritten Query:
"""

    rewritten = await LLMClient.generate_answer(prompt)

    clean_query = rewritten.replace('"', '').replace("'", "").replace("Search Query:", "").strip()

    state["rewritten_query"] = clean_query

    return state