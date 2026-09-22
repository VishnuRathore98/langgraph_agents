import operator
from typing import Annotated, Literal, TypedDict

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from rich import print

from config import settings

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    temperature=0.6,
    max_tokens=1024,
)


class PostState(TypedDict):
    topic: str

    post: str
    evaluation: Literal["approved", "needs_improvement"]
    feedback: str

    post_history: Annotated[list[str], operator.add]
    feedback_history: Annotated[list[str], operator.add]

    current_iteration: int
    max_iterations: int


class EvaluatorModelSchema(BaseModel):
    evaluation: Literal["approved", "needs_improvement"]
    feedback: str


post_evaluator_model = model.with_structured_output(EvaluatorModelSchema)


def generate(state: PostState) -> dict:
    prompt = f"You are an expert content creator write a short 10 lines long social media post for linkedin on the topic: {state['topic']}"
    result = model.invoke(prompt).content

    return {"post": result, "post_history": [result]}


def evaluate(state: PostState) -> dict:
    prompt = f"You are a social media post evaluator, the user has created a post on: {state['topic']}, the content is {state['post']}, evaluate the post and share your feedback and evaluation of the post as 'approved' or 'needs_improvement'.Never approve in the first evaluation."

    result = post_evaluator_model.invoke(prompt)

    return {
        "feedback": result.feedback,
        "evaluation": result.evaluation,
        "feedback_history": [result.feedback],
    }


def optimize(state: PostState) -> dict:
    prompt = f"You are a social media post optimizer, the user has written a post {state['post']}, the expert evaluator has provided its feedback on it: {state['feedback']}, now based on the feedback you have to improve upon the base post so that it can be approved by the evaluator."
    result = model.invoke(prompt).content

    current_iteration = state["current_iteration"] + 1

    return {
        "post": result,
        "post_history": [result],
        "current_iteration": current_iteration,
    }


def check_evaluation_condition(
    state: PostState,
) -> Literal["approved", "needs_improvement"]:
    if (
        state["evaluation"] == "approved"
        or state["current_iteration"] >= state["max_iterations"]
    ):
        return "approved"
    else:
        return "needs_improvement"


graph = StateGraph(PostState)

graph.add_node("generate_post", generate)
graph.add_node("evaluate_post", evaluate)
graph.add_node("optimize_post", optimize)

graph.add_edge(START, "generate_post")
graph.add_edge("generate_post", "evaluate_post")
graph.add_conditional_edges(
    "evaluate_post",
    check_evaluation_condition,
    {"approved": END, "needs_improvement": "optimize_post"},
)
graph.add_edge("optimize_post", "evaluate_post")

workflow = graph.compile()

initial_state = {
    "topic": "Value of coins in the Indian market.",
    "max_iterations": 5,
    "current_iteration": 1,
}

result = workflow.invoke(initial_state)

print(result)
