### **Workshop Agenda: Build Your Own Chatbot**
**Date**: 20.09.2024  
**Time**: 8:00 AM - 4:00 PM

---

**8:00 AM - 8:20 AM**  
**Welcome and Introduction (20 min)**
* Welcome
* Overview of the day’s agenda
* Workshop goal
* Brief overview of NVIDIA Jetson Orin Nano, Development Env and Goal Architecture
* Startup development environment with NVIDIA Jetson Orin Nano

---

### **Session 1: Introduction to LLMs**

**8:30 AM - 8:50 AM**  
**Theory (30 min)**
* GenAI and Foundation Models
* Large Language Models (LLMs): General concept
* Usage of LLMs: One Shot, Few Shot, Fine Tuning for task solving
* ChatModels: Fine Tuned LLMs with conversations
* Basics of prompt engineering (Prompt Structure)
* Deployment of LLMs (Docker, Ollama) on Nvidi Jetson Orin Nano
* Interaction with deployed LLM

**8:50 AM - 9:40 AM**  
**Practical (45 min)**
* Deploy LLM on Orin with Ollama and Docker
* Writing and executing simple prompts using HTTP Client and Python
* Experimenting with prompt techniques and observing LLM responses

---

**9:40 AM - 9:50 AM**  
**Coffee Break (10 min)**

---

### **Session 2: Introduction to LangChain**

**9:50 AM - 10:10 AM**  
**Theory (30 min)**
* LangChain Ecosystem
* Introduction to LangChain
* Key Components of LangChain

**10:10 AM - 11:00 AM**  
**Practical (45 min)**
* Creating a simple Chain in LangChain (using Jupyter Notebook)
* Connecting multiple prompts, processing responses, and building a basic chatbot flow

---

**11:00 AM - 11:10 AM**  
**Coffee Break (10 min)**

---

### **Session 3: Retrieval-Augmented Generation (RAG)**

**11:10 AM - 11:30 AM**  
**Theory (30 min)**
* Introduction to Retrieval-Augmented Generation (RAG)
* Vector Embeddings
* Vector Databases
* Retrieval (Vectore Search)

**11:30 AM - 12:20 PM**  
**Practical (45 min)**
* Setting up a Vector Database (e.g., ChromaDB) in Jupyter Notebook
* Loading custom data into the database and creating embeddings
* Performing similarity searches using vector queries to retrieve contextually relevant information

---

**12:20 PM - 1:00 PM**  
**Lunch Break (60 min)**

---

### **Session 4: Building a RAG-Chain in LangChain**

**1:00 PM - 1:20 PM**  
**Theory (?? min)**
* Combining retrieval mechanisms with generation tasks in LangChain
* Building a RAG-Chain: Integrating the Vector Database with LLM for context-aware responses

**1:20 PM - 2:10 PM**  
**Practical (?? min)**
* Implementing a RAG-Chain in LangChain (using Jupyter Notebook)
* Enhancing chatbot responses with context injection from the Vector Database

---

**2:10 PM - 2:20 PM**  
**Break (10 min)**

---

### **Session 5: Building the Chat Application**

**2:20 PM - 2:40 PM**  
**Theory (?? min)**
* Overview of the target architecture
* Introduction to the building blocks of the chatbot application

**2:40 PM - 4:00 PM**  
**Practical (?? min)**
* Implementing the architecture: Setting up the frontend using Gradio and the backend with FastAPI
* Integrating the chatbot into the application
* Testing the chatbot and debugging issues

---

**4:00 PM**
**End of Workshop**


#### Tag 2: Vertiefung Chatbot

Gruppenarbeit, Endepräsentation

Erweiterungs Ideen:

- Automation Data Integration (RAG)
- Speech Integration
- Answer Rating vom User (User in the loop)
- Multimodaler Ansatz im Chat
- Beispiel Klausuren generieren mit Template wird gefüllt
- Multi Agent Szenario (Researcher -> retriever, Question Generator (wissensfrage, transferfrage), Qualitäts Prüfungs Agent)
-> Technische Beispiel


Eigene Ideen:

- Studierende überlegen sich eigene Ideen / Features