from backend.app.core.llm_client import LLMClient


async def formatter_node(state):

    question = state["question"]
    context = state.get("context", [])

    context_text = "\n".join([
        f"- {c.get('title', 'Property')}: {c.get('summary', 'Details available upon request.')}"
        for c in context[:10]
    ])

    prompt = f"""
You are a Stockland Real Estate expert. 
Base your answer ONLY on the context provided. If no info is found, say you can't find specific details but offer to help find a community.
Context:
{context_text}
User: {question}
Rule: Be concise. Use **bold** for prices and names.
"""

    answer = await LLMClient.generate_answer(prompt)

    state["answer"] = answer

    return state