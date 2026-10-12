from deepagents import create_deep_agent
from langchain_openrouter import ChatOpenRouter
from rich import print

from chat_agent.config import settings

model = ChatOpenRouter(
    model=settings.OPEN_ROUTER_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    temperature=0,
    max_tokens=1000,
)

agent = create_deep_agent(
    model=model,
    system_prompt="You are a helpful agent. Do what user asks you to do.",
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Read the file 'README.md', what is written in it ?",
            }
        ]
    }
)

print(result)
