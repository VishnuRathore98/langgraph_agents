import operator
from typing import Annotated, TypedDict

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from rich import print

from config import settings

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    temperature=0,
    max_tokens=1024,
)


class EvaluationSchema(BaseModel):
    feedback: str = Field(
        description="Concise, short and honest feedback for the essay."
    )
    score: float = Field(
        description="Score for the essay quality, out of 10.", ge=0, le=10
    )


class EssayState(TypedDict):
    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str

    overall_feedback: str
    individual_scores: Annotated[list[float], operator.add]
    average_score: float


structured_model = model.with_structured_output(EvaluationSchema)
# result = structured_model.invoke(prompt)


def evaluate_language(state: EssayState) -> dict:
    pass


def evaluate_analysis(state: EssayState) -> dict:
    pass


def evaluate_thought(state: EssayState) -> dict:
    pass


def final_evaluation(state: EssayState) -> dict:
    pass


graph = StateGraph(EssayState)

graph.add_node()

graph.add_edge()

workflow = graph.compile()

essay = ""

initial_state = {"essay": essay}

result = workflow.invoke(initial_state)

print(result)
