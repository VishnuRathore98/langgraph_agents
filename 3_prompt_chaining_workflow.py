from typing import TypedDict

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, StateGraph

from config import settings

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    max_tokens=1024,
    temperature=0,
)


class BlogPost(TypedDict):
    title: str
    outline: str
    blog: str


def generate_outline(state: BlogPost) -> BlogPost:

    title = state["title"]
    prompt = f"Based on the title: {title}, create a short outline for a blog."

    state["outline"] = model.invoke(prompt).content

    # Why to return state?
    # Because returning state cause state update in langgraph nodes using reducers.
    # If a node doesn't return anything, Python implicitly returns None,
    # and LangGraph merges None into the state instead of your changes —
    # so your update gets lost.
    return state


def generate_blog(state: BlogPost) -> BlogPost:

    title = state["title"]
    outline = state["outline"]

    prompt = (
        f"Based on the title: {title}, and outline: {outline}, create a short blog."
    )

    state["blog"] = model.invoke(prompt).content

    return state


graph = StateGraph(BlogPost)

graph.add_node("generate_outline", generate_outline)
graph.add_node("generate_blog", generate_blog)

graph.add_edge(START, "generate_outline")
graph.add_edge("generate_outline", "generate_blog")
graph.add_edge("generate_blog", END)

workflow = graph.compile()

initial_state = {"title": "State of coding in AI era"}

response = workflow.invoke(initial_state)

print(response)
