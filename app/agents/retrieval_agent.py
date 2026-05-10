from app.rag.workflows import build_langgraph_workflow


class RetrievalAgent:
    def __init__(self) -> None:
        self.workflow = build_langgraph_workflow()

    async def plan(self, question: str) -> dict[str, object]:
        if self.workflow is None:
            return {"question": question, "strategy": "hybrid"}
        return await self.workflow.ainvoke({"question": question})

