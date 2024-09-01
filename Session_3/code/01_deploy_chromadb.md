#### Task: Set Up a Vector Database (e.g., ChromaDB) with Docker

**Objective:**
Set up and configure a vector database using Docker to store and manage vector embeddings efficiently.

**Task Description:**
In this task, you will pull the Docker image for ChromaDB. You will then create and configure a container for ChromaDB, ensuring it is properly set up to interact with your Python environment in the Jupyter Notebook. This setup will be the foundation for storing and retrieving vector embeddings in subsequent tasks.

**How to:**

Running Chroma server locally can be achieved via a simple docker command as shown below.

```
docker run -d --rm --name chromadb -v ./chroma:/chroma/chroma -e IS_PERSISTENT=TRUE -e ANONYMIZED_TELEMETRY=TRUE chromadb/chroma:latest
```

- -v specifies a local dir which is where Chroma will store its data so when the container is destroyed the data remains. Note: If you are using -e PERSIST_DIRECTORY then you need to point the volume to that directory.
- -e IS_PERSISTENT=TRUE let’s Chroma know to persist data
- -e PERSIST_DIRECTORY=/path/in/container specifies the path in the container where the data will be stored, by default it is /chroma/chroma
- -e ANONYMIZED_TELEMETRY=TRUE allows you to turn on (TRUE) or off (FALSE) anonymous product telemetry which helps the Chroma team in making informed decisions about Chroma OSS and commercial direction.
- chromadb/chroma:latest indicates the latest Chroma version but can be replaced with any valid tag if a prior version is needed (e.g. chroma:0.4.24)