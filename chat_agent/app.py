import streamlit as st
from agent import HumanMessage, chatbot
from ulid import ULID

st.title("Agent Neo", text_alignment="center")
st.sidebar.title("Your Chat History")

user_input = st.chat_input("Ask anything...")

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def add_thread():
    chat_id = str(ULID())
    st.session_state["chat_history"].append(chat_id)
    return chat_id


config = {"configurable": {"thread_id": "1"}}

# thread_id = add_thread()

# Feature under development
if st.sidebar.button(label="New Chat"):
    chat_id = add_thread()
    config = {"configurable": {"thread_id": chat_id}}
    for chat in st.session_state["chat_history"]:
        st.sidebar.text(chat)

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
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

    st.session_state["message_history"].append(
        {"role": "assistant", "content": assistant_response}
    )
