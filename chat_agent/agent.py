from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from rich import print
from ulid import ULID

from config import settings

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    temperature=0.6,
    max_tokens=1024,
)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chatbot_node(state: ChatState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


thread_id = str(ULID())
config = {"configurable": {"thread_id": thread_id}}
checkpoint = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chatbot_node", chatbot_node)

graph.add_edge(START, "chatbot_node")
graph.add_edge("chatbot_node", END)

chatbot = graph.compile(checkpointer=checkpoint)

# initial_state = {"messages": "hey, how are you?"}

# result = chatbot.invoke(initial_state)

# print(result)

while True:
    message = input("User: ")
    if message == "exit" or message == "quit":
        break
    result = chatbot.invoke(
        {"messages": [HumanMessage(content=message)]}, config=config
    )
    print(result["messages"][-1].content)
