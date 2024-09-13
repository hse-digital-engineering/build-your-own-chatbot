#### Pre-Installation

- SSD Mount + Docker Installation: [How To](https://www.jetson-ai-lab.com/tips_ssd-docker.html)
- Update System via sudo apt-get update  & sudo apt-get upgrade & sudo apt-get autoremove
- Install Git
- Clone Repo Build your own Chatbot to /ssd
- Install Python
- Install rye
- Install VSCode
- Install recommended VSCode Extensions
- Install jtop

**VSCode Extensions:**

```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "esbenp.prettier-vscode",
        "foxundermoon.shell-format",
        "ms-azuretools.vscode-docker",
        "rangav.vscode-thunder-client",
        "mhutchie.git-graph",
        "ms-vscode-remote.remote-containers",
        "ms-python.isort",
        "ms-toolsai.jupyter"
    ]
}
````

Run rye sync in repository to create `.venv` with dependencies.