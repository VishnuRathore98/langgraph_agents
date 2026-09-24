import streamlit as st
from agent import HumanMessage, chatbot, config

st.title("Agent Neo", text_alignment="center")

user_input = st.chat_input("Ask anything...")

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

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
