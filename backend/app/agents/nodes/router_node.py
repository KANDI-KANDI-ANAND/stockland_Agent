def router(state):
    intents = state.get("intent", ["search"])
    
    targets = []

    for intent in intents:
        if intent in ["communities", "homes", "news", "ads", "releases", "report", "submit_interest"]:
            targets.append(intent)
        else:
            targets.append("search")
    
    return targets
