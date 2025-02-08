import os
import streamlit as st
from datetime import datetime
from streamlit.logger import get_logger
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#decorator
def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):

        # to clear chat history after swtching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def configure_llm():
    available_llms = ["llama3.1:3b","llama3.2:1b"]
    llm_opt = st.sidebar.radio(
        label="LLM",
        options=available_llms,
        key="SELECTED_LLM"
        )

    if llm_opt == "llama3.1:8b":
        llm = ChatOllama(model="llama3.1", base_url=st.secrets["OLLAMA_ENDPOINT"])
    elif llm_opt == "llama3.2:3b":
        llm = ChatOllama(model="llama3.2", base_url=st.secrets["OLLAMA_ENDPOINT"])
    else:
        llm = ChatOllama(model="llama3.1", base_url=st.secrets["OLLAMA_ENDPOINT"])
    return llm

def print_qa(question, answer):
    log_str = "\nQuestion: {}\nAnswer: {}\n" + "------"*10
    logger.info(log_str.format(question, answer))

@st.cache_resource
def configure_embedding_model():
    #embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    #return embedding_model
    return None

def sync_st_session():
    for k, v in st.session_state.items():
        st.session_state[k] = v