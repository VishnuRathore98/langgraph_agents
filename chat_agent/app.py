import streamlit as st
from agent import HumanMessage, chatbot
from rich import print
from ulid import ULID

st.title("Agent Neo", text_alignment="center")
st.sidebar.title("Your Chat History")

user_input = st.chat_input("Ask anything...")

if "chat_sessions" not in st.session_state:
    st.session_state["chat_sessions"] = {}
    st.session_state["chat_sessions"][str(ULID())] = []


if "current_chat" not in st.session_state:
    st.session_state["current_chat"] = list(st.session_state["chat_sessions"].keys())[
        -1
    ]


def add_thread():
    chat_id = str(ULID())
    st.session_state["chat_sessions"][chat_id] = []
    # print("All available sessions: ", st.session_state["chat_sessions"])
    return chat_id


def select_chat(chat_id: str, chat_history: list):
    # print("current selected chat: ", (chat_id, chat_history))
    st.session_state["current_chat"] = chat_id


if st.sidebar.button(label="New Chat"):
    chat_id = add_thread()
    st.session_state["current_chat"] = chat_id


for chat_id, chat_history in st.session_state["chat_sessions"].items():
    st.sidebar.button(
        label=chat_id,
        type="tertiary",
        on_click=select_chat,
        args=(chat_id, chat_history),
    )

# print("",st.session_state["current_chat"])
config = {"configurable": {"thread_id": st.session_state["current_chat"]}}

for message in st.session_state["chat_sessions"][st.session_state["current_chat"]]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

if user_input:
    st.session_state["chat_sessions"][st.session_state["current_chat"]].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("human"):
        st.text(user_input)

    with st.chat_message("assistant"):
        assistant_response = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": HumanMessage(content=user_input)},
                config=config,
                stream_mode="messages",
            )
        )

    st.session_state["chat_sessions"][st.session_state["current_chat"]].append(
        {"role": "assistant", "content": assistant_response}
    )
    # print(st.session_state["chat_sessions"])
