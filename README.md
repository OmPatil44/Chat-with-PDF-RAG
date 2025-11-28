# ``99% Vibe Coded | Trial of AntiGravity``
---

# Research RAG Assistant

A fully local, decoupled RAG application for chatting with research papers.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **RAG**: LangChain (LCEL), ChromaDB, Ollama
- **Database**: SQLite

## Prerequisites
- Python 3.9+
- Ollama running with `gemma:2b` model (`ollama run gemma:2b`)

## Setup & Running

### 1. Install Dependencies
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Start Backend
```powershell
$env:PYTHONPATH='backend'; .\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Start Frontend
Open a new terminal:
```powershell
.\venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

## Usage
1.  Open `http://localhost:8501`.
2.  Click **"New Session"**.
3.  Upload a PDF research paper.
4.  Click **"Ingest Document"**.
5.  Chat with your document!
