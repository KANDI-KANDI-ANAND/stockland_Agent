from langgraph.graph import StateGraph, END

from backend.app.agents.agent_graph import AgentState
from backend.app.agents.nodes.intent_node import intent_node
from backend.app.agents.nodes.router_node import router

from backend.app.agents.nodes.search_node import search_node
from backend.app.agents.nodes.communities_node import communities_node
from backend.app.agents.nodes.homes_node import homes_node
from backend.app.agents.nodes.news_node import news_node
from backend.app.agents.nodes.ads_node import ads_node
from backend.app.agents.nodes.releases_node import releases_node
from backend.app.agents.nodes.query_rewrite_node import query_rewrite_node
from backend.app.agents.nodes.formatter_node import formatter_node
from backend.app.agents.nodes.submit_interest_node import submit_interest_node
from backend.app.agents.nodes.report_node import report_node


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("intent", intent_node)
    graph.add_node("rewrite", query_rewrite_node)
    graph.add_node("search", search_node)
    graph.add_node("communities", communities_node)
    graph.add_node("homes", homes_node)
    graph.add_node("news", news_node)
    graph.add_node("ads", ads_node)
    graph.add_node("releases", releases_node)
    graph.add_node("formatter", formatter_node)
    graph.add_node("submit_interest", submit_interest_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("intent")

    graph.add_edge("intent", "rewrite")

    graph.add_conditional_edges(
        "rewrite",
        router,
        {
            "search": "search",
            "communities": "communities",
            "homes": "homes",
            "news": "news",
            "ads": "ads",
            "releases": "releases",
            "submit_interest": "submit_interest",
            "report": "report",
        },
    )
    graph.add_edge("search", "formatter")
    graph.add_edge("communities", "formatter")
    graph.add_edge("homes", "formatter")
    graph.add_edge("news", "formatter")
    graph.add_edge("ads", "formatter")
    graph.add_edge("releases", "formatter")

    graph.add_edge("formatter", END)

    return graph.compile()