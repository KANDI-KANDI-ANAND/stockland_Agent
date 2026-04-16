from typing import TypedDict, Any


class AgentState(TypedDict):

    question: str
    rewritten_query: str
    intent: str
    context: str
    answer: str
    history: list
    db: Any
    lead: dict