from typing import TypedDict

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, StateGraph

from config import settings

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    temperature=0,
    api_key=settings.OPEN_ROUTER_API_KEY,
    max_tokens=1024,
)


class LLMState(TypedDict):
    question: str
    answer: str


def llm_qa(state: LLMState) -> LLMState:

    question = state["question"]
    prompt = f"Please answer in short user's question: {question}"

    response = model.invoke(prompt).content

    state["answer"] = response

    return state


graph = StateGraph(LLMState)

graph.add_node("llm_qa", llm_qa)

graph.add_edge(START, "llm_qa")
graph.add_edge("llm_qa", END)

workflow = graph.compile()

initial_state = {
    "question": "How many planets are there in milkyway galaxy, as of 2026?"
}

response = workflow.invoke(initial_state)

print(response["answer"])
