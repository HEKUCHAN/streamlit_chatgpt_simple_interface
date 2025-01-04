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

if prompt := st.chat_input("送信するメッセージを入力"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.chat.completions.create(
        messages=st.session_state["messages"],
        model=settings.openai_model,
    )

    assistant_message = response.choices[0].message.content
    st.session_state["messages"].append(
        {"role": "assistant", "content": assistant_message}
    )
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
