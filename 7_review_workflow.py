from typing import Literal, TypedDict

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from rich import print

from config import settings

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    temperature=1.5,
    max_tokens=1024,
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
        description="The category of issue mentioned in the review"
    )
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(
        description="The emotional tone expressed by the user"
    )
    urgency: Literal["low", "medium", "high"] = Field(
        description="How urget or critical the issue appears to be"
    )


structured_sentiment_model = model.with_structured_output(SentimentSchema)
structured_diagnosis_model = model.with_structured_output(DiagnosisSchema)


def find_sentiment(state: ReviewState) -> dict:
    prompt = f"Here's the user's review on my product {state['review']}, could you please do a sentiment analysis of this review and share whether it is a 'positive' or 'negative' review."
    sentiment = structured_sentiment_model.invoke(prompt).sentiment

    return {"sentiment": sentiment}


def check_condition(
    state: ReviewState,
) -> Literal["run_diagnosis", "positive_response"]:
    if state["sentiment"] == "negative":
        return "run_diagnosis"
    else:
        return "positive_response"


def run_diagnosis(state: ReviewState) -> dict:
    prompt = f"The user has provided a negative review on my product: {state['review']}, could you please help me diagnose the review and to better assist the user, please provide me user's issue_type, tone, and the urgency of the user's response."
    diagnosis = structured_diagnosis_model.invoke(prompt).model_dump()

    return {"diagnosis": diagnosis}


# prompt = f"The user has provided a negative review on my product: the product is not fullfilling the requiemtns of our services, the customers are not able to access the user portal to check their recent purchases history, could you please help me diagnose the review and to better assist the user, please provide me user's issue_type, tone, and the urgency of the user's response."
# diagnosis = structured_diagnosis_model.invoke(prompt)
# print(diagnosis)


def negative_response(state: ReviewState) -> dict:
    prompt = f"The user has provided a negative review: {state['review']}, the issue type is: {state['diagnosis']['issue_type']}, the user's tone is: {state['diagnosis']['tone']}, the urgency of the issue is {state['diagnosis']['urgency']}. Could you please respond to the user in an assertive, responsive and make the user confident that their response is recorded and the team is looking into it with atmost priority and will respond back soo."
    response = model.invoke(prompt).content

    return {"response": response}


def positive_response(state: ReviewState) -> dict:
    prompt = f"The user has provided a good positive review: {state['review']}. Could you please respond to the user properly thanking them for their response and using our product. The user should feel good about the feedback."
    response = model.invoke(prompt).content

    return {"response": response}


graph = StateGraph(ReviewState)

graph.add_node("find_sentiment", find_sentiment)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("negative_response", negative_response)
graph.add_node("positive_response", positive_response)

graph.add_edge(START, "find_sentiment")
graph.add_conditional_edges("find_sentiment", check_condition)
graph.add_edge("run_diagnosis", "negative_response")
graph.add_edge("positive_response", END)
graph.add_edge("negative_response", END)

workflow = graph.compile()

positive_initial_state = {
    "review": "I've been using this speaker for about two weeks and I'm really impressed. The sound is clear, the bass is surprisingly good for its size, and the battery easily lasts through my workday. Pairing was quick and hassle-free. Definitely worth the price."
}
response = workflow.invoke(positive_initial_state)
print("Positive review: \n\n", response)

negative_initial_state = {
    "review": "Very disappointing product. The battery barely lasts three hours, Bluetooth disconnects randomly, and the sound becomes distorted at higher volume. The buttons also feel cheap. I wouldn't recommend it."
}
response = workflow.invoke(negative_initial_state)
print("Negative review: \n\n", response)

neutral_initial_state = {
    "review": "The speaker looks good and is compact enough to carry around easily. The sound is decent at normal volume, although the bass could be better. Battery life has been somewhere around five to six hours for me. It works fine overall, but I'm not sure I'd buy it again at the current price."
}
response = workflow.invoke(neutral_initial_state)
print("Neutral review: \n\n", response)
