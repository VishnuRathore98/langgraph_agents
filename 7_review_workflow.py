from typing import Literal, TypedDict

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from rich import print

from config import settings

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    temperature=0.2,
)


class Diagnosis(TypedDict):
    issue_type: Literal["ui", "performance", "bug", "support", "other"]
    tone: Literal["angry", "frustrated", "disappointed", "calm"]
    urgency: Literal["low", "medium", "high"]


class ReviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: Diagnosis

    response: str


class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="Sentiment of the review"
    )


class DiagnosisSchema(BaseModel):
    issue_type: Literal["ui", "performance", "bug", "support", "other"] = Field(
        description=""
    )
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description="")
    urgency: Literal["low", "medium", "high"] = Field(description="")


def find_sentiment(state: ReviewState) -> dict:
    pass


def run_diagnosis(state: ReviewState) -> dict:
    pass


def negative_response(state: ReviewState) -> dict:
    pass


def positive_response(state: ReviewState) -> dict:
    pass


graph = StateGraph(ReviewState)

graph.add_node("find_sentiment", find_sentiment)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("negative_response", negative_response)
graph.add_node("positive_response", positive_response)

graph.add_edge(START, "find_sentiment")
graph.add_edge("", END)

workflow = graph.compile()

initial_state = {"review": ""}

response = workflow.invoke(initial_state)

print(response)
