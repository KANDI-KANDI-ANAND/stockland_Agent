import json # Make sure to import json at the top
from backend.app.core.llm_client import LLMClient

async def formatter_node(state):
    question = state["question"]
    context = state.get("context", [])

    # NEW LOGIC: Convert every item to JSON so zero data is lost
    context_text = "\n".join([json.dumps(c) for c in context])

    prompt = f"""
You are a Stockland Real Estate Presentation Expert. 

TASK:
- Format the provided Data into a professional, easy-to-read response.
- Use **bold headings** and bullet points.
- If an item has an 'image_url', you MUST display it as: ![Property Image](url).

DATA TO PROCESS:
{context_text}

User Question: {question}
"""

    answer = await LLMClient.generate_answer(prompt)
     
    return {"answer": answer}
