import os
import streamlit as st
from openai import OpenAI

# ----------------------------
# Model Configuration
# ----------------------------
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=st.secrets["HF_TOKEN"],
)

MODEL_NAME = "Qwen/Qwen3-Coder-30B-A3B-Instruct:nebius"

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot (with Memory)")

# Initialize session memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant that remembers the conversation."}
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to session
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate model response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=st.session_state.messages,
                )
                reply = completion.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ API Error: {e}"

            st.markdown(reply)

    # Add assistant response to memory
    st.session_state.messages.append({"role": "assistant", "content": reply})
