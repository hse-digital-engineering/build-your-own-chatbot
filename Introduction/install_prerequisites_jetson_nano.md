### Pre-Installation

> Check if the Orin has the correct date: Execute `date` on a terminal.

1. **System Update & Cleanup**  
   Run the following commands to ensure the system is up to date:
   ```bash
   sudo apt-get update && sudo apt-get upgrade && sudo apt-get autoremove
   ```

2. **Install Required Tools**
   - **Git**:
     ```bash
     sudo apt-get install git
     ```
   - **Python**:
     ```bash
     sudo apt-get install python3 python3-pip
     ```
   - **VSCode**: [Install Visual Studio Code](https://code.visualstudio.com/Download)
     ```bash
     wget -N -O vscode-linux-deb.arm64.deb https://update.code.visualstudio.com/latest/linux-deb-arm64/stable
     sudo apt install ./vscode-linux-deb.arm64.deb
     ```
   - **Jtop** (for Jetson systems monitoring):
     ```bash
     sudo -H pip3 install -U jetson-stats
     sudo reboot
     ```
   - **Docker** (should be already installed, permissions for user is missing)
   ```bash
   sudo groupadd docker
   sudo usermod -aG docker $USER
   sudo chmod 666 /var/run/docker.sock
   ```

4. **Install Rye**  
   Install Rye, a Python toolchain manager:
   ```bash
   curl -sSf https://rye.astral.sh/get | bash
   echo 'source "$HOME/.rye/env"' >> ~/.bashrc
   ```

   Use:
   
   - UV as dependency manager 
   - python version managed by rye: 3.11

5. **Clone Repository**
   Clone your chatbot project to the SSD:
   ```bash
   mkdir /home/johbaum8/DEV
   cd /home/johbaum8/DEV
   git clone <repo-url>
   ```

6. **VSCode Setup**
   - **Install Recommended Extensions**: Add the following extensions to your VSCode settings for a smooth development environment.
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
     ```
   - Install these extensions automatically by running:
     ```bash
     code --install-extension ms-python.python
     code --install-extension ms-python.vscode-pylance
     code --install-extension esbenp.prettier-vscode
     code --install-extension foxundermoon.shell-format
     code --install-extension ms-azuretools.vscode-docker
     code --install-extension rangav.vscode-thunder-client
     code --install-extension mhutchie.git-graph
     code --install-extension ms-vscode-remote.remote-containers
     code --install-extension ms-python.isort
     code --install-extension ms-toolsai.jupyter
     ```

7. **Set Up Virtual Environment & Dependencies**
   Navigate to the project directory and sync dependencies:
   ```bash
   cd /home/johbaum8/DEV/build-your-own-chatbot
   rye sync
   ```