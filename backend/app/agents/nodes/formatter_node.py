from backend.app.core.llm_client import LLMClient


async def formatter_node(state):

    question = state["question"]
    context = state.get("context", [])

    context_text = "\n".join([
        f"- {c.get('type','Item').upper()}: {c.get('title')}. Info: {c.get('summary')}. "
        f"{'[IMAGE_URL: ' + c.get('image_url') + ']' if c.get('image_url') else ''}"
        for c in context
    ])

    prompt = f"""
You are a Stockland Real Estate Expert and Consultant. 
Base your answer ONLY on the context provided. If no info is found, say you can't find specific details but offer to help find a community.
ROLE & STYLE:
- Base your answer ONLY on the context provided.
- Be proactive: Compare the options in the context and provide a **Suggestion** if the user asks for a recommendation or seems unsure.
- If the user has a specific requirement (like area size or price), explain WHY a specific property is a good fit.
VISUAL RULE:
- If an item has an [IMAGE_URL: url], you MUST display that image using Markdown format: ![Property Image](url).
CONVERSATIONAL RULES:
- Be concise but helpful. 
- Use **bold** for prices, community names, and key features.
- If no info is found, offer to help find a general Stockland community.
Context:
{context_text}
User: {question}
"""

    answer = await LLMClient.generate_answer(prompt)

    state["answer"] = answer

    return state