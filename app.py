import streamlit as st
from openai import OpenAI
import time

# Setup API client
token = st.secrets["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Page setup
st.set_page_config(page_title="OpenAI Coding Chatbot", layout="centered")
st.title("🧠 Chat with GPT-4.1 Nano")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-4.1 Nano model to answer coding questions, "
    "but can be used for other purposes."
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if "message_times" not in st.session_state:
    st.session_state.message_times = []
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

# Function to check rate limit
def is_rate_limited():
    current_time = time.time()
    # Keep timestamps from past 60 seconds
    st.session_state.message_times = [
        t for t in st.session_state.message_times if current_time - t < 60
    ]
    return len(st.session_state.message_times) >= 20

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Your message:"):
    if is_rate_limited():
        st.warning("⚠️ Rate limit exceeded: Please wait a moment before sending more messages.")
    elif prompt == st.session_state.last_prompt:
        st.info("🤖 You've already sent that message.")
    else:
        st.session_state.last_prompt = prompt
        st.session_state.message_times.append(time.time())

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query the model
        response = client.chat.completions.create(
            messages=st.session_state.messages,
            temperature=1,
            top_p=1,
            model=model
        )

        # Display assistant response
        assistant_reply = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
