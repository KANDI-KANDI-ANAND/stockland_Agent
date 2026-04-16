def router(state):

    lead = state.get("lead", {})
    if lead and any(lead.values()):
        return "submit_interest"

    intent = state["intent"]
    question = state["question"].lower()

    if intent == "communities":
        return "communities"

    if intent == "homes":
        return "homes"

    if intent == "news":
        return "news"

    if intent == "ads":
        return "ads"

    if intent == "releases":
        return "releases"

    if intent == "report":
        return "report"

    if intent == "submit_interest":
        return "submit_interest"

    if "report" in question or "pdf" in question:
        return "report"
    
    if any(k in question for k in ["buy", "contact", "call me", "interested in buying"]):
        return "submit_interest"

    return "search"