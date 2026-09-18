from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


# Define state
class ModerationState(TypedDict):
    post_content: str
    user_reputation: str

    formatted_post: str
    content_flag: str
    result: str


# Define nodes methods
def formal_post(state: ModerationState) -> dict:
    pass


def analyze_content(state: ModerationState) -> dict:
    pass


def check_condition(
    state: ModerationState,
) -> Literal["approve_post", "flag_for_review", "reject_post"]:
    pass


def approve_post(state: ModerationState) -> dict:
    pass


def flag_for_review(state: ModerationState) -> dict:
    pass


def reject_post(state: ModerationState) -> dict:
    pass


# Declare graph
graph = StateGraph(ModerationState)

# Create nodes from methods
graph.add_node("formal_post", formal_post)
graph.add_node("analyze_content", analyze_content)

graph.add_node("approve_post", approve_post)
graph.add_node("flag_for_review", flag_for_review)
graph.add_node("reject_post", reject_post)

# Connect nodes to form graph
graph.add_edge(START, "formal_post")
graph.add_edge("formal_post", "analyze_content")

graph.add_conditional_edges("analyze_content", check_condition)

graph.add_edge("approve_post", END)
graph.add_edge("flag_for_review", END)
graph.add_edge("reject_post", END)

# Compile graph
workflow = graph.compile()

# Define Initial state
initial_state = {"": ""}

# Invoke graph
response = workflow.invoke(initial_state)

print(response)
