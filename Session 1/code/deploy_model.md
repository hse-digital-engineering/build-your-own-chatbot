## Deploying a Large Language Model (LLM) on Nvidia Orin using Ollama

To deploy a Large Language Model (LLM) on an Nvidia Orin device locally, we use **Ollama**. This tool allows us to efficiently run LLMs leveraging the Nvidia GPU capabilities of the Orin platform.

### Overview

**Ollama** is a framework designed for running large language models locally. When deploying on an Nvidia Orin device, Ollama takes advantage of the Nvidia GPU through Docker containers. The Nvidia Container Toolkit enables Docker to use GPU acceleration, which is critical for the performance of LLMs.

### Steps for Deployment

#### 1. Install the Nvidia Container Toolkit

The Nvidia Container Toolkit is necessary for Docker to interact with the GPU on the Orin device. This toolkit ensures that Docker containers can leverage GPU resources for computation.

**Installation Guide:**
Follow the steps in the official Nvidia documentation: [Nvidia Container Toolkit Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation).

#### 2. Configure Docker to Use the Nvidia Runtime

Once the Nvidia Container Toolkit is installed, you need to configure Docker to use the Nvidia runtime. This step ensures that the Docker container can access the GPU.

Run the following commands in the terminal:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

- The first command configures Docker to use Nvidia's GPU runtime.
- The second command restarts the Docker service to apply the configuration changes.

#### 3. Run Ollama Inside a Docker Container

Next, you'll need to pull the Ollama Docker image from the Docker Hub registry and run it on your Orin device. This container will serve as the environment for deploying and managing your LLM.

**Commands:**

1. **Pull the Ollama Docker Image:**

   ```bash
   docker pull ollama/ollama
   ```

   This command fetches the latest Ollama image from the public Docker Hub registry.

2. **Run the Ollama Container:**

   ```bash
   docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

   - `-d`: Runs the container in detached mode (in the background).
   - `--gpus=all`: Allocates all available GPUs to the container.
   - `-v ollama:/root/.ollama`: Mounts a volume for persistent storage, ensuring data inside the container is not lost.
   - `-p 11434:11434`: Maps port 11434 on the host to port 11434 in the container, allowing access to the Ollama service.
   - `--name ollama`: Names the container "ollama" for easy management.

#### 4. Run the Llama 3 Model Inside the Container

With the Ollama container running, you can now execute the Llama 3 model. This step involves using Ollama's command interface to start the LLM within the container.

**Command:**

```bash
docker exec -it ollama ollama run llama3
```

- `docker exec -it ollama`: Accesses the running Ollama container.
- `ollama run llama3`: Executes the Llama 3 model within the container.

### Conclusion

By following these steps, you can deploy and run a Large Language Model on the Nvidia Orin platform using Ollama. This setup leverages Nvidia's GPU acceleration to handle the computational demands of LLMs, ensuring efficient model performance.