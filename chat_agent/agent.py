import sqlite3
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from rich import print

# pyrefly: ignore [missing-import]
from tools import calculator_tool, stock_price_tool, weather_tool, web_search_tool

from config import settings

load_dotenv()

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    temperature=0.6,
    max_tokens=1024,
)

tools = [
    calculator_tool,
    stock_price_tool,
    weather_tool,
    web_search_tool,
]

model = model.bind_tools(tools=tools)

# print(calculator_tool(2, 3, "addition"))


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chatbot_node(state: ChatState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


tools = ToolNode(tools=tools)


conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)

# checkpoint = MemorySaver()
checkpoint = SqliteSaver(conn)

graph = StateGraph(ChatState)

graph.add_node("chatbot_node", chatbot_node)
graph.add_node("tools", tools)

graph.add_edge(START, "chatbot_node")
graph.add_conditional_edges("chatbot_node", tools_condition)
graph.add_edge("tools", "chatbot_node")
graph.add_edge("chatbot_node", END)

chatbot = graph.compile(checkpointer=checkpoint)

threads = checkpoint.list(config=None)

threads_set = set()
for thread in threads:
    threads_set.add(thread.config["configurable"]["thread_id"])

# res = model.invoke("How are you?")
# print(res)
