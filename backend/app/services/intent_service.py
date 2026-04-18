from backend.app.core.llm_client import LLMClient


class IntentService:

    @staticmethod
    async def detect_intent(question: str, history: list = []):

        history_context = "\n".join([f"{m['role']}: {m['content']}" for m in history[-3:]])

        prompt = f"""
Classify the user's intents based on the conversation history and message.
INSTRUCTIONS:
- If the user has MULTIPLE requests (e.g., asking for news AND homes), return both separated by a comma.
- Example: 'homes, news' or 'communities, ads'.
- If only one intent, return just one.
Possible intents:
search, communities, homes, news, ads, releases, submit_interest, report
Return ONLY the intent name(s) separated by commas if multiple.
"""

        response = await LLMClient.generate_answer(prompt)

        return response.strip().lower()