from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB client
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    ssl=False,
    headers=None,
    settings=Settings(allow_reset=True, anonymized_telemetry=False),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)
collection = client.get_or_create_collection("ai_model_book")

vector_db_from_client = Chroma(
    client=client,
    collection_name="ai_model_book",
    embedding_function=embedding_function,
)

# Create ChromaDB retriever and agent tool

retriever = vector_db_from_client.as_retriever()

tool = create_retriever_tool(
    retriever,
    "search_custom_document",
    "Searches and returns information from custom docs.",
)
tools = [tool]

# SQLite-backed conversation memory
# chat_message_history = SQLChatMessageHistory(
#     session_id="test_session_id", connection_string="sqlite:///sqlite.db"
# )

# Initialize Ollama's Chat model
llm = ChatOllama(model="sam4096/qwen2tools:1.5b")

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise."),
#          MessagesPlaceholder("chat_history", optional=True),
#         ("human", "{input}"),
#         MessagesPlaceholder("agent_scratchpad"),
#     ]
# )

# Create an agent for question-answering with retrieval
# agent = create_tool_calling_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

prompt_template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

<context>
{context}
</context>

Answer the following question:

{question}"""

rag_prompt = ChatPromptTemplate.from_template(prompt_template)

retriever = vector_db_from_client.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

qa_rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print('CONNECTING...')
    while True:
        try:
            input_data = await websocket.receive_text()
            print(input_data)
            #agent_result = await agent_executor.ainvoke({"input": input_data})
            chain_result = await qa_rag_chain.ainvoke(input_data)
            print(chain_result)
            await websocket.send_text(chain_result)
        except Exception as e:
            print(e)
            break
    print("CONNECTION DEAD...")


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)