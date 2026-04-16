from backend.app.core.llm_client import LLMClient


async def query_rewrite_node(state):

    question = state["question"]
    history = state.get("history", [])

    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history[-3:]])

    prompt = f"""
Given the following conversation history and the new user message, rewrite the user message into a standalone, descriptive search query.
HISTORY:
{history_text}
USER MESSAGE:
{question}
EXAMPLE:
History: AI asks "Want more info on Highlands?"
User: "Yes"
Output: "Provide more details about Highlands community location and amenities"
Rewritten Query:
"""

    rewritten = await LLMClient.generate_answer(prompt)

    state["rewritten_query"] = rewritten.strip()

    return state