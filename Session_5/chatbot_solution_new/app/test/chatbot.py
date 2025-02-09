

import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables import RunnableSerializable
from langchain_core.load.serializable import Serializable
from langchain_chroma import Chroma
from chromadb.api import ClientAPI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import re
from uuid import uuid4
import logging
import os

OLLAMA_HOST_NAME = os.environ.get("OLLAMA_HOST_NAME", "localhost")
CHROMA_HOST_NAME = os.environ.get("CHROMA_HOST_NAME", "localhost")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "bge-m3")
MODEL_NAME = os.environ.get("MODEL_NAME", "llama3.2:1B")

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console logs
    ],
)

logger = logging.getLogger(__name__)

class CustomChatBot:
    """
    A class representing a chatbot that uses a ChromaDB client for document retrieval
    and the ChatOllama model for generating answers.

    This chatbot uses a retrieval-augmented generation (RAG) pipeline where it retrieves
    relevant information from a custom document database (ChromaDB) and then generates
    concise answers using a language model (ChatOllama).
    """

    def __init__(self, index_data: bool, pull_embedding_model: bool) -> None:
        """
        Initialize the CustomChatBot class by setting up the ChromaDB client for document retrieval
        and the ChatOllama language model for answer generation.
        """

        # Initialize the embedding function for document retrieval
        if pull_embedding_model:
            self._pull_embedding_model()
        self.embedding_function = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=f"http://{OLLAMA_HOST_NAME}:11434")

        # Initialize the ChromaDB client
        self.client = self._initialize_chroma_client()
        
        # Get or create the document collection in ChromaDB
        self.vector_db = self._initialize_vector_db()

        # Process pdf, embedd data and index to ChromaDB
        if index_data:
            self._index_data_to_vector_db()

        # Initialize the document retriever
        self.retriever = self.vector_db.as_retriever(k=3)

        # Initialize the large language model (LLM) from Ollama
        self.llm = ChatOllama(model=MODEL_NAME, base_url=f"http://{OLLAMA_HOST_NAME}:11434")

        # Initialize Memory
        self.msgs = StreamlitChatMessageHistory()
        self.memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=self.msgs, return_messages=True)

        # Set up the retrieval-augmented generation (RAG) pipeline
        self.qa_rag_chain = self._initialize_qa_rag_chain()

    def _pull_embedding_model(self):
        logger.info(f"Pull embedding model {EMBEDDING_MODEL}")
        try:

            response = requests.post(f"http://{OLLAMA_HOST_NAME}:11434/api/pull", json = {"name": EMBEDDING_MODEL,  "stream": False})
            response.raise_for_status()
            logger.info(response.json())
        except:
            raise

    def _initialize_chroma_client(self) -> ClientAPI:
        """
        Initialize and return a ChromaDB HTTP client for document retrieval.

        Returns:
            chromadb.HttpClient: A client used to communicate with ChromaDB.
        """ 
        logger.info("Initialize chroma db client.")
        return chromadb.HttpClient(
            host=CHROMA_HOST_NAME,
            port=8000,
            ssl=False,
            settings=Settings(allow_reset=True, anonymized_telemetry=False),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE
        )

    def _initialize_vector_db(self) -> Chroma:
        """
        Initialize and return a Chroma vector database using the HTTP client.

        Returns:
            Chroma: A vector database instance connected to the document collection in ChromaDB.
        """
        logger.info("Initialize chroma vector db.")
        return Chroma(
            client=self.client,
            collection_name="ai_model_book",
            embedding_function=self.embedding_function
        )
    
    def _index_data_to_vector_db(self):

        pdf_doc = "src/AI_Book.pdf"

        # Create pdf data loaders
        loader = PyPDFLoader(pdf_doc)

        # Load and split documents in chunks
        pages_chunked = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter())

        # Function to clean text by removing invalid unicode characters, including surrogate pairs
        def clean_text(text):
            # Remove surrogate pairs
            text = re.sub(r'[\ud800-\udfff]', '', text)
            # Optionally remove non-ASCII characters (depends on your use case)
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            return text

        pages_chunked_cleaned = [clean_text(chunk.page_content) for chunk in pages_chunked]

        uuids = [str(uuid4()) for _ in range(len(pages_chunked_cleaned[10:50]))]

        self.vector_db.add_documents(documents=pages_chunked[10:50], ids=uuids)

    def _initialize_qa_rag_chain(self) -> RunnableSerializable[Serializable, str]:

        qa_chain = ConversationalRetrievalChain.from_llm(
            self.llm, retriever=self.retriever, memory=self.memory, verbose=True
        )
        return qa_chain
        
    async def astream(self, question: str):
        """
        Handle a user query asynchronously by running the question through the RAG pipeline and stream the answer.

        Args:
            question (str): The user's question as a string.

        Yields:
            str: The generated answer from the model, streamed chunk by chunk.
        """
        logger.info("Streaming RAG chain response.")
        try:
            async for chunk in self.qa_rag_chain.astream(question):
                logger.debug(f"Yielding chunk: {chunk}")
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream_answer: {e}", exc_info=True)
            raise