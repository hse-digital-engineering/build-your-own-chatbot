## Deploying a Large Language Model (LLM) on Jetson Orin Nano with Ollama

### Overview

This guide provides a streamlined approach to deploying and running a Large Language Model (LLM) on the Jetson Orin Nano using Ollama, a powerful framework for running LLMs locally. You will learn how to set up the environment, deploy a pre-built Docker container, and interact with the model inside the container.

<<<<<<< HEAD
For detailed documentation, refer to: [Jetson AI Lab Ollama Tutorial](https://www.jetson-ai-lab.com/tutorial_ollama.html).

---

### Deployment Steps Using a Pre-Built Container

1. Pull the Docker image:
   ```bash
   docker pull dustynv/ollama:r35.4.1
   ```

2. Run the container:
   ```bash
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama dustynv/ollama:r35.4.1
   ```

3. Execute the model inside the running container:
   ```bash
   docker exec -it ollama ollama run sam4096/qwen2tools:1.5b
   ```

---

### Steps for Building and Deployment from scratch

> Use this when working on jetpack 5. dustynv/ollama:r36.2.0 only works on jetpack 6

#### 1. Clone the Container Repository

The first step is to clone the repository containing the Jetson-compatible containers. This repository provides pre-built containers optimized for Nvidia Jetson devices, including the Orin Nano.

Run the following command to clone the repository:
=======
For more detailed documentation, visit the official guide here: [Jetson AI Lab Ollama Tutorial](https://www.jetson-ai-lab.com/tutorial_ollama.html).

---

### Building and Deploying the Ollama Container from Scratch

#### 1. Clone the Container Repository

Start by cloning the repository that contains Jetson-compatible Docker containers, optimized for Nvidia Jetson devices.
>>>>>>> feature/optimizations

```bash
git clone https://github.com/dusty-nv/jetson-containers
```

<<<<<<< HEAD
This command will download the `jetson-containers` repository to your local machine, allowing you to access and use the container configurations specific to Jetson devices.

#### 2. Install the Containers

After cloning the repository, you'll need to run the installation script provided within the repository. This script installs all the necessary components and prepares your system to run the containers.

Run the installation script with:
=======
This repository includes pre-configured containers designed for the Jetson Orin Nano and other Jetson devices.

#### 2. Install the Containers

Next, install the necessary dependencies and prepare your environment by running the installation script provided in the repository.
>>>>>>> feature/optimizations

```bash
bash jetson-containers/install.sh
```

<<<<<<< HEAD
This script sets up the environment, installs dependencies, and configures the system to work with the containers designed for Jetson devices.

#### 3. Run the Ollama Container

Once the installation is complete, you can run the Ollama container. The container is designed to leverage the Jetson Orin Nano's capabilities, providing an optimized environment for running LLMs.

Use the following command to start the container (root directory and terminal outside VS-Code):

```bash
jetson-containers run --name ollama $(autotag ollama)
```

- `jetson-containers run`: This command launches the container using the configurations provided by the `jetson-containers` repository.
- `--name ollama`: This option names the container "ollama" for easy identification.
- `$(autotag ollama)`: Automatically tags and pulls the latest Ollama container image compatible with the Jetson Orin Nano.

### Manually Download and Run a LLM in the Ollama Container

To manually download and run a specific LLM model, such as Llama 3.1, inside the Ollama container, use the following command:

TODO Hinweis Mario: Es ist unklar, ob man in einem Container ist oder ausserhalb (gibt es in der Command Line dazu Möglichkeiten, dass der Teilnehmer dies sehen kann? Würde zum erstmaligen Verständnis besser sein)

```bash
docker exec -it ollama ollama run sam4096/qwen2tools:1.5b
```

- `docker exec -it ollama`: Executes commands inside the running Ollama container.
- `ollama run sam4096/qwen2tools:1.5b`: Runs the specified model (`sam4096/qwen2tools:1.5b`) within the container.
=======
This script will install required components and configure your system for running LLMs in Docker containers on Jetson hardware.

#### 3. Run the Ollama Container

Now you can start the Ollama container, optimized for Jetson Orin Nano. To do so, use the following command from the terminal (outside VS Code):

```bash
jetson-containers run --name ollama $(autotag ollama) -Y
```

- `jetson-containers run`: Starts the container using configurations from the cloned repository.
- `--name ollama`: Names the container "ollama" for easy identification.
- `$(autotag ollama)`: Automatically tags and pulls the latest Ollama container image optimized for Jetson Orin Nano.

The container's shell should launch after this command.

---

### Manually Download and Run a LLM in the Ollama Container

To manually download and run a model like Llama 3.2 inside the Ollama container, use the following command outside the container shell:

```bash
docker exec -it ollama ollama run llama3.2
```

If you are already inside the container shell, you can simply run:

```bash
ollama run llama3.2
```

---

### Automatically Download and Run a LLM in the Ollama Container

You can also automatically download and run the LLM model using this command:

```bash
jetson-containers run $(autotag ollama) bash -c "/bin/ollama serve & sleep 5; ollama run llama3"
```
>>>>>>> feature/optimizations

---

### Access the Container Shell

<<<<<<< HEAD
For more control or troubleshooting, you might want to access the container's shell directly. This allows you to interact with the container's file system and manually manage models or configurations.

Enter the container's shell using:
=======
To troubleshoot or manage the container manually, access its shell using:
>>>>>>> feature/optimizations

```bash
docker exec -it ollama sh
```

<<<<<<< HEAD
This command opens an interactive shell session within the Ollama container.
=======
This opens an interactive shell within the running Ollama container.
>>>>>>> feature/optimizations

---

### Interact with Ollama in the Container Shell

<<<<<<< HEAD
Once inside the container's shell, you can interact with Ollama using its command-line interface (CLI). Below is an overview of the basic usage and available commands.

#### Basic Usage:
=======
Once inside the container, you can interact with Ollama via its CLI. Here are some basic commands:

#### General Command Format:
>>>>>>> feature/optimizations

```bash
ollama [command] [flags]
```

#### Available Commands:

- **serve**: Start Ollama's service.
- **create**: Create a model from a Modelfile.
<<<<<<< HEAD
- **show**: Display information about a model.
=======
- **show**: Display model information.
>>>>>>> feature/optimizations
- **run**: Execute a model.
- **pull**: Download a model from a registry.
- **push**: Upload a model to a registry.
- **list**: List all available models.
- **ps**: List currently running models.
- **cp**: Copy a model.
- **rm**: Remove a model.
- **help**: Get help for any command.

#### Example Commands:

1. **Run a Model**:
   ```bash
<<<<<<< HEAD
   ollama run sam4096/qwen2tools:1.5b
=======
   ollama run llama3.2
>>>>>>> feature/optimizations
   ```

2. **List Available Models**:
   ```bash
   ollama list
   ```

3. **Pull a Model from a Registry**:
   ```bash
<<<<<<< HEAD
   ollama pull sam4096/qwen2tools:1.5b
   ```
=======
   ollama pull llama3.2
   ```

---

### Alternative Deployment Using a Pre-Built Container

Alternatively, you can pull a pre-built Ollama container from Docker Hub: [dustynv/ollama](https://hub.docker.com/r/dustynv/ollama).

Pre-built images are available for different Jetpack versions:

- **Jetpack 5**: `dustynv/ollama:r35.4.1`
- **Jetpack 6**: `dustynv/ollama:r36.4.0`

#### Steps:

1. **Check the installed Jetpack version**:

   ```bash
   sudo apt-cache show nvidia-jetpack
   ```

2. **Pull the appropriate Docker image** based on your Jetpack version:

   ```bash
   docker pull dustynv/ollama:r36.4.0
   ```

3. **Run the container**:

   ```bash
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama dustynv/ollama:r36.4.0
   ```

4. **Execute the model inside the running container**:

   ```bash
   docker exec -it ollama ollama run llama3.2
   ```

---
>>>>>>> feature/optimizations
