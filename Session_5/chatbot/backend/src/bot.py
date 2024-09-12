import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from uuid import uuid4
from typing import List
import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

# Gerüst stehen lassen -> Transfer von Session 4 zu 5

class CustomChatBot:
    """
    A class representing a chatbot that uses a ChromaDB client for document retrieval
    and the ChatOllama model for generating answers.

    This chatbot uses a retrieval-augmented generation (RAG) pipeline where it retrieves
    relevant information from a custom document database (ChromaDB) and then generates
    concise answers using a language model (ChatOllama).
    """

    def __init__(self) -> None:
        """
        Initialize the CustomChatBot class by setting up the ChromaDB client for document retrieval
        and the ChatOllama language model for answer generation.
        """
        # Initialize the embedding function for document retrieval
        self.embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        
        # Initialize the ChromaDB client
        self.client = self._initialize_chroma_client()
        
        # Get or create the document collection in ChromaDB
        self.vector_db = self._initialize_vector_db()

        # Process pdf, embedd data and index to ChromaDB
        self._index_data_to_vector_db()

        # Initialize the document retriever
        self.retriever = self.vector_db.as_retriever()

        # Initialize the large language model (LLM) from Ollama
        self.llm = ChatOllama(model="sam4096/qwen2tools:1.5b", base_url="http://ollama:11434")

        # Set up the retrieval-augmented generation (RAG) pipeline
        self.qa_rag_chain = self._initialize_qa_rag_chain()

    def _initialize_chroma_client(self) -> chromadb.HttpClient:
        """
        Initialize and return a ChromaDB HTTP client for document retrieval.

        Returns:
            chromadb.HttpClient: A client used to communicate with ChromaDB.
        """
        logger.info("Initialize chroma db client.")
        return chromadb.HttpClient(
            host="chroma",
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

        pdf_doc = "/app/src/AI_Book.pdf"

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

        uuids = [str(uuid4()) for _ in range(len(pages_chunked_cleaned[:50]))]

        self.vector_db.add_documents(documents=pages_chunked[:50], ids=uuids)

    def _initialize_qa_rag_chain(self) -> dict:
        """
        Set up the retrieval-augmented generation (RAG) pipeline for answering questions.
        
        The pipeline consists of:
        - Retrieving relevant documents from ChromaDB.
        - Formatting the retrieved documents for input into the language model (LLM).
        - Using the LLM to generate concise answers.
        
        Returns:
            dict: The RAG pipeline configuration.
        """
        logger.info("Initialize rag chain.")
        prompt_template = """
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

        <context>
        {context}
        </context>

        Answer the following question:

        {question}"""

        # Define the prompt template for generating answers
        rag_prompt = ChatPromptTemplate.from_template(prompt_template)

        # Build the RAG pipeline using the retriever and LLM
        return (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | rag_prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_docs(self, docs: List[dict]) -> str:
        """
        Helper function to format the retrieved documents into a single string.
        
        Args:
            docs (List[dict]): A list of documents retrieved by ChromaDB.

        Returns:
            str: A string containing the concatenated content of all retrieved documents.
        """
        return "\n\n".join(doc.page_content for doc in docs)

    async def ainvoke(self, question: str) -> str:
        """
        Handle a user query asynchronously by running the question through the RAG pipeline.
        
        Args:
            question (str): The user's question as a string.

        Returns:
            str: The generated answer from the model as a string.
        """
        logger.info("Async invoke rag chain.")
        return await self.qa_rag_chain.ainvoke(question)