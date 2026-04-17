import os
import streamlit as st
import requests
import time


API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/api/chat")

st.set_page_config(
    page_title="Stockland AI Assistant",
    page_icon="🏡",
    layout="centered"
)

st.markdown("""
<style>
    /* 1. This centers and narrows the main container */
    .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin: auto;
    }
    /* 2. This forces the chat bubbles to stay centered */
    [data-testid="stChatMessageContainer"] {
        max-width: 800px;
        margin: auto;
    }
    /* 3. This is the MAGIC fix: It forces long words to break and wrap */
    [data-testid="stChatMessage"] {
        max-width: 800px;
        margin: auto;
        overflow-wrap: break-word;
        word-wrap: break-word;
        word-break: break-word;
    }
</style>
""", unsafe_allow_html=True)

if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

st.title("🏡 Stockland AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"], avatar=msg["avatar"]):
        st.markdown(msg["content"])


# Chat input
user_prompt = st.chat_input("Ask about communities, homes, reports...")

if user_prompt:

    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt, "avatar": "👤"}
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)

    # Assistant response placeholder
    with st.chat_message("assistant", avatar="🤖"):

        message_placeholder = st.empty()

        with st.spinner("Analyzing Stockland Data..."):
            try:
                response = requests.post(
                    API_URL, 
                    json={
                        "message": user_prompt,
                        "session_id": st.session_state.session_id
                    }
                )
                response.raise_for_status()
                data = response.json()
                answer = data.get("answer", "Sorry, I couldn't process that.")
                # Only try to stream if we actually got an answer
                def stream_data():
                    for word in answer.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                message_placeholder.write_stream(stream_data)
                # Store assistant response in history
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "avatar": "🤖"}
                )
            except Exception as e:
                st.error(f"⚠️ Could not reach the backend: {e}")
                # Provide a fallback so it doesn't crash
                answer = "Error connecting to service."