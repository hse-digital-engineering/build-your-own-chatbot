# Chatbot Solution

This project is a chatbot application designed to run on multiple platforms, including Jetson Nano, Linux, Windows, and MacOS. It consists of both a backend and frontend, as well as additional services like Chroma and Ollama, for processing and managing the chatbot's tasks.

## Requirements

- [Docker](https://docs.docker.com/get-docker/) (ensure Docker and Docker Compose are installed)

## Quick Start

You can easily start the chatbot application by following the steps below for your respective platform.

### Run Chatbot Application

#### On Jetson Nano:

To run the chatbot on a Jetson Nano, use the following command:

```bash
docker compose -f docker-compose-jetson.yml up --build
```

#### On Linux, Windows, or MacOS:

To run the chatbot on Linux, Windows, or MacOS, use the following command:

```bash
docker compose -f docker-compose.yml up --build
```

This command will build and run the chatbot using the appropriate Docker Compose configuration for your system.

## Folder Structure

Here is a detailed explanation of the project's folder structure:

```bash
.
├── chatbot/
│   ├── backend/
│   │   ├── Dockerfile.backend      # Dockerfile for building the backend service
│   │   ├── main.py                 # Entry point for the backend chatbot logic
│   │   ├── pyproject.toml          # Python project configuration for backend
│   │   ├── requirements-dev.lock   # Backend development dependency lock file
│   │   ├── requirements.lock       # Backend production dependency lock file
│   │   └── src/
│   │       ├── AI_Book.pdf         # Documentation or reference material (e.g., book on AI)
│   │       ├── __init__.py         # Marks the `src` directory as a Python module
│   │       └── bot.py              # Core logic of the chatbot, including AI-related operations
│   ├── docker-compose-jetson.yml   # Docker Compose configuration for running on Jetson Nano
│   ├── docker-compose.yml          # Docker Compose configuration for Linux, Windows, and MacOS
│   ├── frontend/
│   │   ├── Dockerfile.frontend      # Dockerfile for building the frontend service
│   │   ├── app.py                   # Entry point for the frontend, handling user interaction
│   │   ├── pyproject.toml           # Python project configuration for frontend
│   │   ├── requirements-dev.lock    # Frontend development dependency lock file
│   │   └── requirements.lock        # Frontend production dependency lock file
│   └── run_chatbot_app.md           # Instructions for running the chatbot application
```

### Explanation of Folders and Files:

- **chatbot/backend/**: Contains the backend code and dependencies. This is where the core logic for the chatbot, including AI processing, resides.
    - **Dockerfile.backend**: Dockerfile used to build the backend service.
    - **main.py**: Main entry point for the backend. It likely initializes the chatbot and handles FastApi websocket backend.
    - **pyproject.toml**: Configuration for the Python project in the backend, including dependencies.
    - **requirements-dev.lock**: Lock file for development dependencies of the backend.
    - **requirements.lock**: Lock file for production dependencies of the backend.
    - **src/**: The source code directory for the backend.
        - **AI_Book.pdf**: A reference document used in the chatbot.
        - **__init__.py**: Makes the `src` folder a Python package.
        - **bot.py**: Contains the chatbot logic, likely handling conversations, AI interaction, and business logic.

- **docker-compose-jetson.yml**: Docker Compose file specifically for running the application on a Jetson Nano device.
  
- **docker-compose.yml**: Docker Compose file for running the application on Linux, Windows, or MacOS.

- **chatbot/frontend/**: Contains the frontend code and dependencies. The frontend handles user interaction, likely through a web or mobile interface.
    - **Dockerfile.frontend**: Dockerfile used to build the frontend service.
    - **app.py**: Main entry point for the frontend application, possibly a web server or user interface for interacting with the chatbot.
    - **pyproject.toml**: Configuration for the Python project in the frontend, including dependencies.
    - **requirements-dev.lock**: Lock file for development dependencies of the frontend.
    - **requirements.lock**: Lock file for production dependencies of the frontend.



### Explanation of the Docker Compose File

Below is an explanation of the `docker-compose.yml` file, which defines how the chatbot application and its supporting services will run inside Docker containers.

```yaml
version: '3'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.frontend
    ports:
      - "7860:7860"
    container_name: frontend
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.backend
    ports:
      - "5001:5001"
    container_name: backend
    depends_on:
      - chroma
      - ollama
    networks:
      - app-network

  chroma:
    image: ghcr.io/chroma-core/chroma
    volumes:
      - ./chroma:/chroma/.chroma/index
    ports:
      - "8000:8000"
    container_name: chroma
    networks:
      - app-network

  ollama:
    image: dustynv/ollama:r36.2.0
    ports:
      - 11434:11434
    volumes:
      - ./ollama/ollama:/root/.ollama
    container_name: ollama
    tty: true
    command: >
      sh -c "ollama serve & ollama run sam4096/qwen2tools:1.5b"
    environment:
      - OLLAMA_KEEP_ALIVE=24h
      - OLLAMA_HOST=0.0.0.0
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Explanation of Services

1. **frontend**:
   - **Build**: The frontend service is built from the `frontend` directory, using `Dockerfile.frontend`.
   - **Ports**: Exposes port `7860` to allow access to the frontend on your local machine.
   - **Depends On**: Ensures that the backend service starts first, as the frontend relies on it.
   - **Networks**: The frontend is part of the `app-network`, which allows it to communicate with the other services.

2. **backend**:
   - **Build**: The backend service is built from the `backend` directory using `Dockerfile.backend`.
   - **Ports**: Exposes port `5001` to allow backend operations, such as API requests.
   - **Depends On**: The backend service depends on `chroma` and `ollama`, meaning these services must be up before the backend starts.
   - **Networks**: The backend is also part of the `app-network`.

3. **chroma**:
   - **Image**: The `chroma` service uses an official Docker image from `ghcr.io`.
   - **Volumes**: Maps the local `./chroma` directory to the container's index storage path, ensuring persistent data.
   - **Ports**: Exposes port `8000`, allowing external access to the `chroma` service.
   - **Networks**: Connected to the `app-network`.

4. **ollama**:
   - **Image**: Uses the `ollama` service from the `dustynv/ollama:r36.2.0` image.
   - **Ports**: Exposes port `11434`, where `ollama` operates.
   - **Volumes**: Maps the local `./ollama/ollama` directory to the container's Ollama configuration directory for persistent storage.
   - **Command**: Runs `ollama serve` (to start the server) and `ollama run` to execute a specific AI model (`sam4096/qwen2tools:1.5b`).
   - **Environment**: Configures `OLLAMA_KEEP_ALIVE` to 24 hours and binds Ollama to host `0.0.0.0` to ensure it listens on all network interfaces.
   - **Networks**: Connected to the `app-network`.

### Network Configuration

- **app-network**:
  - A **bridge** network that allows the different services (frontend, backend, chroma, ollama) to communicate with each other while running in isolated containers. This provides a virtual internal network for seamless interaction between services.


This setup provides a modular architecture where each component of the chatbot application (frontend, backend, and AI services) runs in its own container, ensuring scalability and ease of management. 