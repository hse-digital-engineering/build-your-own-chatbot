import streamlit as st
import asyncio
import logging
from langchain.schema import ChatMessage
from src.chatbot import CustomChatBot
import os

INDEX_DATA = os.environ.get("INDEX_DATA", 0)
PULL_EMBEDDING_MODEL = os.environ.get("PULL_EMBEDDING_MODEL", 0)
# Configure logger
logger = logging.getLogger(__name__)

# Initialize chatbot instance (avoid reloading)
if "bot" not in st.session_state:
    st.session_state["bot"] = CustomChatBot(index_data=bool(INDEX_DATA), pull_embedding_model=bool(PULL_EMBEDDING_MODEL))

# Streamlit UI setup
st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.header("Chat with your documents (Basic RAG)")
st.write("Has access to custom documents and can respond to user queries by referring to the content within those documents.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

# Handle user input
if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.session_state.messages.append(ChatMessage(role="user", content=user_query))
    st.chat_message("user").write(user_query)

    async def handle_user_query(user_query):
        container = st.empty()
        answer = ""

        try:
            async for event in st.session_state["bot"].qa_rag_chain.astream_events(user_query, version="v2"):
                if event.get("event") == "on_chat_model_stream":
                    chunk = event['data']['chunk'].content
                    if chunk:
                        answer += chunk
                        container.markdown(answer)  # Updates incrementally
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            container.error("An error occurred while processing your request.")

        # Store assistant response in session state
        if answer:
            st.session_state.messages.append(ChatMessage(role="assistant", content=answer))

    with st.chat_message("assistant"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(handle_user_query(user_query))