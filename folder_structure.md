# Research RAG Assistant - Folder Structure

This document outlines the modular directory structure for the decoupled Full-Stack RAG application.

```
RP-RAG/
├── backend/                  # FastAPI Backend
│   ├── app/
│   │   ├── api/              # API Endpoints
│   │   │   ├── routers/
│   │   │   │   ├── chat.py       # Chat endpoints (POST /chat)
│   │   │   │   ├── documents.py  # Document upload/management (POST /upload)
│   │   │   │   └── session.py    # Session management endpoints
│   │   │   └── deps.py       # Dependency injection (DB session, etc.)
│   │   ├── core/             # Core application config
│   │   │   ├── config.py     # Environment variables & settings
│   │   │   └── exceptions.py # Custom exception handlers
│   │   ├── db/               # Database Layer (SQLite)
│   │   │   ├── base.py       # SQLAlchemy declarative base
│   │   │   ├── session.py    # Async DB session factory
│   │   │   └── models.py     # SQL models (ChatHistory, Sessions)
│   │   ├── rag/              # RAG Service Layer
│   │   │   ├── embeddings.py # Embedding model initialization
│   │   │   ├── vector_store.py # ChromaDB client & collection management
│   │   │   ├── ingestion.py  # Async PDF processing & chunking
│   │   │   └── chain.py      # LangChain retrieval & generation logic
│   │   └── main.py           # FastAPI entry point
│   ├── requirements.txt      # Backend dependencies
│   └── .env                  # Backend environment variables
│
├── frontend/                 # Streamlit Frontend
│   ├── components/           # UI Components
│   │   ├── chat.py           # Chat interface components
│   │   ├── sidebar.py        # Sidebar for file uploads & session info
│   │   └── utils.py          # Helper functions (API calls)
│   ├── app.py                # Streamlit entry point
│   └── .streamlit/
│       └── config.toml       # Streamlit configuration
│
├── data/                     # Persistent Data Storage
│   ├── chroma/               # ChromaDB persistence directory
│   └── sqlite/               # SQLite database file (rag.db)
│
├── tests/                    # Automated Tests
│   ├── backend/
│   └── frontend/
│
├── docs/                     # Documentation
│   ├── project_plan.md
│   ├── folder_structure.md
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## Key Modules Description

- **backend/app/rag/ingestion.py**: Handles asynchronous loading of PDFs, text splitting, and vectorization.
- **backend/app/rag/vector_store.py**: Manages ChromaDB interactions, including metadata filtering for session isolation.
- **backend/app/db/models.py**: Defines SQLite schemas for storing chat history and session metadata.
- **frontend/components/utils.py**: Contains functions to communicate with the FastAPI backend via `httpx`.
