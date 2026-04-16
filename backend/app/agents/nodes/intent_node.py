from backend.app.services.intent_service import IntentService


async def intent_node(state):

    question = state["question"]
    history = state.get("history", [])

    intent = await IntentService.detect_intent(question, history)

    state["intent"] = intent.strip().lower()

    return state