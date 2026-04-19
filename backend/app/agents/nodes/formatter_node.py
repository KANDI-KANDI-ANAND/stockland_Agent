import json 
from backend.app.core.llm_client import LLMClient

async def formatter_node(state):
    question = state["question"]
    context = state.get("context", [])

    context_text = "\n".join([json.dumps(c) for c in context])

    prompt = f"""
You are a Stockland Real Estate Presentation Expert. 

TASK:
- Format the provided Data into a professional, easy-to-read response.
- Use **bold headings** and bullet points.
- If an item has an 'image_url', you MUST display it as: ![Property Image](url).
- **CRITICAL**: If you see a [Download Link] in the data, do not try to re-write it. Just copy and paste it exactly at the end of your message.

DATA TO PROCESS:
{context_text}

User Question: {question}
"""

    answer = await LLMClient.generate_answer(prompt)
     
    return {"answer": answer}
