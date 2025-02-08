from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_community.document_loaders import TextLoader
import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain_ollama.chat_models import ChatOllama
from langchain_text_splitters import CharacterTextSplitter
import requests
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import chromadb
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain.tools.retriever import create_retriever_tool
from uuid import uuid4


st_callback = StreamlitCallbackHandler(st.container())

# Download embedding model
requests.post("http://localhost:11434/api/pull", json = {"name": "bge-m3",  "stream": False})

# Define LLM
llm = ChatOllama(model="llama3.2:1B", base_url="http://ollama:11434")

# Run embedding process

# 1. load raw data and preprocess data
loader = TextLoader("./state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# 2. Define embedding model
embedding_model = OllamaEmbeddings(
    model="bge-m3",
)

# 3. Setup vector data base connection
client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    ssl=False,
    headers=None,
    settings=Settings(allow_reset=True, anonymized_telemetry=False),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

collection = client.get_or_create_collection("data")

vector_db_from_client = Chroma(
    client=client,
    collection_name="data",
    embedding_function=embedding_model,
)


# 4. Run embedding process
uuids = [str(uuid4()) for _ in range(len(texts))]
vector_db_from_client.add_documents(documents=texts, ids=uuids)


# 5. Setup agent tool

retriever = vector_db_from_client.as_retriever()

tool = create_retriever_tool(
    retriever,
    "search_state_of_union",
    "Searches and returns excerpts from the 2022 State of the Union.",
)
tools = [tool]



agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {"input": prompt}, {"callbacks": [st_callback]}
        )
        st.write(response["output"])