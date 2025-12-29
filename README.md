# AI Twin (Local RAG)

This project builds a **local AI Twin** using:
- Ollama (local LLM runner)
- LangChain (LLM orchestration)
- ChromaDB (vector database for RAG)

No cloud APIs. Everything runs locally on Kali Linux.

---

## 📁 Project Structure

ai-twin/
├── ingest.py        # Converts documents into embeddings and stores them in Chroma
├── query.py         # Ask questions to the local LLM using RAG
├── prompts.py       # Prompt templates for the AI
├── data/            # Documents used for knowledge (PDF, TXT, etc.)
├── vectordb/        # Persistent vector database (Chroma)
├── requirements.txt # Python dependencies
├── README.md        # Project documentation

---

## ⚙️ Setup Instructions

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate


3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start Ollama
ollama serve

📥 Index Documents (RAG)

Place your documents inside the data/ folder, then run:

python ingest.py

💬 Query the AI Twin
python query.py


Type exit to quit.

🧠 How It Works

Documents are chunked and embedded using nomic-embed-text

Vectors are stored in ChromaDB

Queries retrieve relevant chunks

Context is passed to a local LLM via Ollama

The model answers only using retrieved context

