import base64
import streamlit as st
from openai import OpenAI

from settings import Settings

settings = Settings()
client = OpenAI(api_key=settings.openai_api_key)

st.title(settings.title)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input(
    "送信するメッセージを入力",
    accept_file="multiple",
    file_type=["png", "jpg", "jpeg"],
):
    with st.chat_message("user"):
        st.markdown(user_message.text)

        if user_message.files:
            for file in user_message.files:
                st.image(file)

    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "user", "content": user_message.text})
        message_placeholder = st.empty()
        message_placeholder.markdown("AIが考え中...")

        full_response = ""

        if user_message.files:
            message = {
                "role": "user",
                "content": [{"type": "text", "text": user_message.text}],
            }
            for file in user_message.files:
                file_bytes = file.read()
                file_encoded_base64 = base64.b64encode(file_bytes).decode("utf-8")
                message["content"].append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{file.type};base64,{file_encoded_base64}"},
                    }
                )

            st.session_state.messages.append(message)
        else:
            st.session_state.messages.append(
                {"role": "user", "content": user_message.text}
            )

        stream = client.chat.completions.create(
            messages=st.session_state["messages"],
            model=settings.openai_model,
            stream=True,
        )

        for chunk in stream:
            full_response += chunk.choices[0].delta.content or ""
            message_placeholder.markdown(full_response)

    st.session_state["messages"].append({"role": "assistant", "content": full_response})
