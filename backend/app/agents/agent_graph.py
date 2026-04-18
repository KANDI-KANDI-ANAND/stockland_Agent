from typing import TypedDict, Any, Annotated
import operator


class AgentState(TypedDict):

    question: str
    rewritten_query: str
    intent: list
    context: Annotated[list, operator.add]
    answer: str
    history: list
    db: Any
    lead: dict