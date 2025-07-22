import os
import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("OpenAI Coding Chatbot")
st.write(
    "This is an AI coding chatbot that uses OpenAI's GP-4.1-nano model to answer coding-related questions. "
    "An API key is automatically provided via the `GITHUB_TOKEN` environment variable, but is rate limited to avoid abuse. "
)

token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

# Create an OpenAI client.
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Typer a message..."):
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
            stream=True,
        )

# Stream the response to the chat using `st.write_stream`, then store it in 
# session state.
with st.chat_message("assistant"):
    response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
