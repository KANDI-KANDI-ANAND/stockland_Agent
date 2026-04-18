from backend.app.services.intent_service import IntentService


async def intent_node(state):

    question = state["rewritten_query"]
    history = state.get("history", [])

    intent_string = await IntentService.detect_intent(question, history)

    intent_list = [i.strip() for i in intent_string.split(",")]

    return {"intent": intent_list} 