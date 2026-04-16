from backend.app.core.llm_client import LLMClient


async def formatter_node(state):

    question = state["question"]
    context = state.get("context", [])

    context_text = "\n".join([
        f"{c.get('name', 'N/A')}: {c.get('description', 'No description available')}"
        for c in context
    ])

    prompt = f"""
You are a helpful assistant for Stockland real estate.
Answer the user's question using the provided context.
STRICT FORMATTING RULES:
1. Use **bold text** for property names, communities, and prices.
2. Use bullet points (-) for any lists of features, ads, or news.
3. Start a new paragraph with a double newline for different topics.
4. If providing a list of items, ensure each item starts on a fresh line.

User Question: {question}
Relevant Information: {context_text}
"""

    answer = await LLMClient.generate_answer(prompt)

    state["answer"] = answer

    return state