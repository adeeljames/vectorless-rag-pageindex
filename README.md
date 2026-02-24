## 📖 Overview

Welcome to the **Agentic Retrieval RAG System**, an end-to-end, production-ready document Q&A application powered by [PageIndex](https://pageindex.ai/). This project demonstrates a paradigm shift in Retrieval-Augmented Generation (RAG). 

Traditional Similarity-based RAG pipelines rely heavily on text chunking, embedding generation, and vector databases, which often lead to context loss and the "lost-in-the-middle" problem. This system utilizes **Vectorless Reasoning-based RAG**, allowing AI to natively read and comprehend entire documents—giving transparent, human-expert-level responses.

## ✨ Key Features

- **Vectorless Agentic Retrieval**: Process massive document contexts without manual chunking, vectors, or external embedding databases.
- **Lightning-Fast Execution**: Environment and dependency management powered by `uv`, the fastest package installer and resolver for Python.
- **Real-Time Streaming**: Tokens stream directly to the chat UI for an interactive, ChatGPT-like experience.
- **Production-Ready Architecture**: Cleanly separated modular design (`app.py` for UI, `src/` for logic & API wrappers).
- **Persistent File Logging**: Beautiful console & rolling file logging via `loguru`.

## 📂 Project Structure

```text
page-index-chat-rag/
├── src/
│   ├── __init__.py        
│   ├── logger.py          # Loguru configuration for console and persistent file logging
│   └── rag_api.py         # Backend logic & PageIndex API integration
├── logs/                  # Auto-generated application logs
├── .env.example           # Example environment variables
├── .gitignore             # Comprehensive python project git ignore
├── app.py                 # Streamlit Frontend application
├── pyproject.toml         # uv Project Configuration
├── uv.lock                # Lockfile for exact dependency reproducibility
└── README.md              # Project Documentation
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh` or `pip install uv`)
- A PageIndex API Key (Get yours at [Dash PageIndex](https://dash.pageindex.ai/api-keys))

### 2. Installation
Clone the repository and install dependencies seamlessly:

```bash
git clone https://github.com/your-username/page-index-chat-rag.git
cd page-index-chat-rag

# Sync dependencies and create an ultra-fast virtual environment
uv sync
```

### 3. Configuration
Copy the example environment variable file and add your API key:
```bash
cp .env.example .env
```
Edit `.env` and insert your API key:
```env
PAGEINDEX_API_KEY=your_pageindex_api_key_here
```

### 4. Run the Application
Activate the virtual environment and launch Streamlit:
```bash
source .venv/bin/activate
streamlit run app.py
```
The interface will automatically open in your browser at `http://localhost:8501`.

## 🧠 How it Works

1. **Upload**: Users upload a PDF securely through the Streamlit UI.
2. **Process**: The backend (`src/rag_api.py`) transmits the file to PageIndex and polls the server until the document parsing is fully resolved.
3. **Chat**: Users submit highly complex, full-document reasoning queries.
4. **Agentic Retrieval**: The underlying PageIndex model completely skips naive top-K chunking. Instead, it natively reads the unstructured file, locates exact pages implicitly, and streams back perfect, context-aware answers.

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Built to showcase modern AI engineering standards.*
