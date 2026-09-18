# deepseek-rag-agent

# 🧠 DeepSeek Code Companion

DeepSeek is an AI-powered code companion designed to assist with coding, debugging, and providing solutions to programming problems. It uses the Ollama API and LangChain framework to generate helpful responses based on user input.
![image](https://github.com/user-attachments/assets/81231bf2-5add-4333-b4b7-50cdd327c5ff)

![image](https://github.com/user-attachments/assets/3266ec64-5e7c-471e-83c1-93e996f06fcc)

![image](https://github.com/user-attachments/assets/63088b66-b517-4b28-b1c7-3a43237ca63c)

![image](https://github.com/user-attachments/assets/465da0be-f4a9-4775-9c74-4235817e6761)

![image](https://github.com/user-attachments/assets/06e1a0e8-113e-4a21-87c9-93c6c74fc936)

![image](https://github.com/user-attachments/assets/88de15bf-d2bf-439e-9d3f-496d4605dccf)

![image](https://github.com/user-attachments/assets/424bc3d3-e9a0-4120-b98d-cc43981e78ec)

![image](https://github.com/user-attachments/assets/a1fcc350-75b3-41e4-9040-4d674e90e6ba)

## 🚀 Features

- **Python Expertise**: Provides solutions, code snippets, and explanations for Python-related queries.
- **Debugging Assistance**: Helps identify and debug issues in your code with useful print statements and suggestions.
- **Code Documentation**: Automatically generates explanations and comments for code.
- **Solution Design**: Offers high-level design and architectural suggestions for software development.

## ⚙️ Prerequisites

Before using this app, make sure you have the following:

- Python 3.7+ installed on your system.
- [Streamlit](https://streamlit.io/) installed (`pip install streamlit`).
- [LangChain](https://python.langchain.com/) installed (`pip install langchain`).
- Ollama's API endpoint running locally on your machine. (You need to install Ollama and run their server on `http://localhost:11434`)

## 🔧 Installation

### 1. Install Dependencies

To get started, install the necessary Python libraries:

```bash
pip install streamlit langchain langchain_ollama
```

### 2. Set up Ollama

Make sure you have Ollama installed and running locally. Visit [Ollama's website](https://ollama.ai/) for detailed instructions on installation and configuration.

### 3. Clone or Download the Repository

Clone the repository (or create a new file) containing your code.

```bash
git clone https://github.com/TanushreeSB/deepseek.git
cd deepseek
```

## 🚀 Running the App

To start the Streamlit app, run:

```bash
streamlit run app.py
```

This will launch the app in your browser at `http://localhost:8501`.

## 🖥️ How It Works

- **User Interaction**: The user types a programming-related question in the input box.
- **AI Response Generation**: The system prompts the Ollama model for an appropriate response, which can be a code solution, debug suggestion, or documentation.
- **Chat Interface**: All interactions are logged and displayed in a chat-like interface, allowing users to have ongoing conversations with the AI assistant.

### Configuration Options
- **Model Selection**: Choose between two pre-configured models: `deepseek-r1:1.5b` or `deepseek-r1:3b`. These models differ in their capability and performance.
- **Customization**: Modify the system prompt to change how the assistant responds (concise, debug-friendly, etc.).

## 💡 Code Explanation

### Streamlit Interface

- **Main UI**: The main user interface displays a chat interface for interacting with the AI assistant. It uses Streamlit's layout capabilities for the chat experience.
  
- **Sidebar**: Contains options to configure the model and other settings.

### Core Components

1. **System Message**: The `system_prompt` defines the AI's behavior, guiding it to act as a concise coding assistant.

2. **Message Log**: All user inputs and AI responses are stored in `st.session_state.message_log`, ensuring the chat history is maintained across interactions.

3. **Chat Interface**: A custom chat interface is created using Streamlit components to display both user and AI messages.

4. **Response Generation**: Upon receiving user input, the app constructs a prompt chain using `LangChain` and sends it to Ollama for processing.

5. **Reset**: A button is provided to clear the chat history and restart the interaction.
