from typing import Any


def build_langgraph_workflow() -> Any | None:
    try:
        from langgraph.graph import END, StateGraph
    except Exception:
        return None

    graph = StateGraph(dict)
    graph.add_node("rewrite_query", lambda state: {**state, "rewritten_query": state["question"]})
    graph.add_node("retrieve", lambda state: state)
    graph.add_node("rerank", lambda state: state)
    graph.add_node("generate", lambda state: state)
    graph.set_entry_point("rewrite_query")
    graph.add_edge("rewrite_query", "retrieve")
    graph.add_edge("retrieve", "rerank")
    graph.add_edge("rerank", "generate")
    graph.add_edge("generate", END)
    return graph.compile()

