from backend.app.core.llm_client import LLMClient


async def query_rewrite_node(state):

    question = state["question"]
    history = state.get("history", [])

    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history[-3:]])

    prompt = f"""
ROLE: You are an expert Search Query Optimizer for a real estate AI.
TASK: Rewrite the user's NEW MESSAGE into a single, standalone search query that includes all necessary context from the HISTORY.
RULES:
1. Resolve all pronouns (it, there, they, those) using the conversation history.
2. Preserve all specific filters: locations, price amounts, bedroom counts, Area (m^2), and property types.
3. Remove conversational noise (hello, please, thanks, I was wondering).
4. Output ONLY the rewritten search query. No sentences, no quotes, no labels.
HISTORY:
{history_text}
NEW MESSAGE: 
{question}
OPTIMIZED SEARCH QUERY:
"""

    rewritten = await LLMClient.generate_answer(prompt)

    clean_query = rewritten.replace('"', '').replace("'", "").replace("Search Query:", "").strip()

    state["rewritten_query"] = clean_query

    return state