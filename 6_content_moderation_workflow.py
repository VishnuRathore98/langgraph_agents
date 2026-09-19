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
    formatted_post = f"User {state['user_reputation']}, says: {state['post_content']}"

    return {"formatted_post": formatted_post}


def analyze_content(state: ModerationState) -> dict:
    content = state["post_content"].lower()

    if "spam" in content or "free" in content or "buy" in content:
        content_flag = "rejected"
    elif state["user_reputation"] == "new_user":
        content_flag = "review"
    else:
        content_flag = "approved"

    return {"content_flag": content_flag}


def check_condition(
    state: ModerationState,
) -> Literal["approve_post", "flag_for_review", "reject_post"]:
    if state["content_flag"] == "rejected":
        return "reject_post"
    elif state["content_flag"] == "review":
        return "flag_for_review"
    else:
        return "approve_post"


def approve_post(state: ModerationState) -> dict:
    result = "Post approved and posted successfully on your timeline."

    return {"result": result}


def flag_for_review(state: ModerationState) -> dict:
    result = "Post is flagged and sent for review."

    return {"result": result}


def reject_post(state: ModerationState) -> dict:
    result = "Post is rejected as it seems violating our policy."

    return {"result": result}


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
# initial_state = {
#     "post_content": "Checkout this new free product!",
#     "user_reputation": "new_user",
# }
# initial_state = {
#     "post_content": "Checkout this new product!",
#     "user_reputation": "new_user",
# }
initial_state = {
    "post_content": "Checkout this new product!",
    "user_reputation": "approved_user",
}

# Invoke graph
response = workflow.invoke(initial_state)

print(response)
