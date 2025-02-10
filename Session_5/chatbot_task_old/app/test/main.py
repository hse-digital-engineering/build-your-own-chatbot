import streamlit as st
import asyncio
import logging
from langchain.schema import ChatMessage
from src.chatbot import CustomChatBot
import os
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

INDEX_DATA = os.environ.get("INDEX_DATA", 0)
PULL_EMBEDDING_MODEL = os.environ.get("PULL_EMBEDDING_MODEL", 0)

# Configure logger
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console logs
    ],
)

logger = logging.getLogger(__name__)


# Initialize chatbot instance (avoid reloading)
if "bot" not in st.session_state:
    st.session_state["bot"] = CustomChatBot(index_data=bool(INDEX_DATA), pull_embedding_model=bool(PULL_EMBEDDING_MODEL))

# Streamlit UI setup
st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.header("Chat with your Document")

if len(st.session_state["bot"].msgs.messages) == 0 or st.sidebar.button("Clear message history"):
    st.session_state["bot"].msgs.clear()
    st.session_state["bot"].msgs.add_ai_message("How can I help you?")

avatars = {"human": "user", "ai": "assistant"}
for msg in st.session_state["bot"].msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

# Handle user input
if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)
    logger.info(f"Write user message in session state {user_query}")

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

    with st.chat_message("assistant"):
        with st.spinner("Searching for information in your documents and generation response..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(handle_user_query(user_query))