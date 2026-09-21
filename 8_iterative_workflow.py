import operator
from typing import Annotated, Literal, TypedDict

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

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


class GeneratorModelSchema(BaseModel):
    pass


class EvaluatorModelSchema(BaseModel):
    pass


class OptimizerModelSchema(BaseModel):
    pass


post_generator_model = model.with_structured_output(GeneratorModelSchema)
post_evaluator_model = model.with_structured_output(EvaluatorModelSchema)
post_optimizer_model = model.with_structured_output(OptimizerModelSchema)
