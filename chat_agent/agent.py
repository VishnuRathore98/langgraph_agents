import sqlite3
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph, add_messages
from rich import print
from langsmith import traceable
from dotenv import load_dotenv

from config import settings

load_dotenv()

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    temperature=0.6,
    max_tokens=1024,
)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


@traceable
def chatbot_node(state: ChatState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)

# checkpoint = MemorySaver()
checkpoint = SqliteSaver(conn)

graph = StateGraph(ChatState)

graph.add_node("chatbot_node", chatbot_node)

graph.add_edge(START, "chatbot_node")
graph.add_edge("chatbot_node", END)

chatbot = graph.compile(checkpointer=checkpoint)

threads = checkpoint.list(config=None)

threads_set = set()
for thread in threads:
    threads_set.add(thread.config["configurable"]["thread_id"])

res = model.invoke("How are you?")
print(res)
# print("Thread set: ", threads_set)
# for thread in threads:
#     print("Thread: ", thread)
# initial_state = {"messages": "hey, how are you?"}

# result = chatbot.invoke(initial_state)

# print(result)

# while True:
#     message = input("User: ")
#     if message == "exit" or message == "quit":
#         break
#     result = chatbot.invoke(
#         {"messages": [HumanMessage(content=message)]}, config=config
#     )
#     print(result["messages"][-1].content)
