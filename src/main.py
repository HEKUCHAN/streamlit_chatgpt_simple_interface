import streamlit as st
from openai import OpenAI

from settings import Settings

settings = Settings()
client = OpenAI(
    api_key=settings.openai_api_key
)

st.title(settings.title)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input("送信するメッセージを入力"):
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "user", "content": user_message})
        message_placeholder = st.empty()
        message_placeholder.markdown("AIが考え中...")

        full_response = ""

        stream = client.chat.completions.create(
            messages=st.session_state["messages"],
            model=settings.openai_model,
            stream=True,
        )

        for chunk in stream:
            full_response += chunk.choices[0].delta.content or ""
            message_placeholder.markdown(full_response)

    st.session_state["messages"].append(
        {"role": "assistant", "content": full_response}
    )
