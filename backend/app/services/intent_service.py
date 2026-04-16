from backend.app.core.llm_client import LLMClient


class IntentService:

    @staticmethod
    async def detect_intent(question: str, history: list = []):

        history_context = "\n".join([f"{m['role']}: {m['content']}" for m in history[-3:]])

        prompt = f"""
Classify the user's intent based on the conversation history and the new message.

RECENT CONVERSATION:
{history_context}
NEW USER MESSAGE: {question}

INSTRUCTIONS:
- If the user says "Yes", "Sure", "Okay", or "Tell me more", check the RECENT CONVERSATION. 
- If the last AI message was about a community, classify as 'communities'.

Possible intents:
search -> general property search questions
communities -> user wants information, details, or overview of a community/location
homes -> asking about specific houses or pricing
news -> asking about news updates
ads -> asking about advertisements
releases -> asking about project releases
submit_interest -> ONLY when user says "I want to buy", "contact me", "call me", or "I'm interested in buying" and If the user says his name and phone number and email address in one message
report -> user specifically asks for a "report" or "PDF"
Examples:
"Tell me about Highlands" -> communities
"What info do you have on Highlands?" -> communities
"I want to buy in Highlands" -> submit_interest
"Call me about Highlands" -> submit_interest
"I have interest in [community name]" -> submit_interest
"My name is John and I want to buy in Highlands" -> submit_interest
"John, 1234567890, [EMAIL_ADDRESS]" -> submit_interest
Return ONLY the intent name.

"""

        response = await LLMClient.generate_answer(prompt)

        return response.strip().lower()