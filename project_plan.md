# Research RAG Assistant - 6-Day Agile Working Plan

This plan outlines the development of a fully local, decoupled RAG application using FastAPI, Streamlit, LangChain, ChromaDB, and SQLite.

## Phase 1: Foundation & Architecture (Days 1-2)

### Day 1: Project Setup & Core Backend
**Goal:** Initialize project, set up environment, and create basic FastAPI shell.
- [ ] **Morning:**
    - Initialize Git repository and directory structure (as per `folder_structure.md`).
    - Set up virtual environment and install dependencies (`requirements.txt`).
    - Configure `backend/app/core/config.py` (Env vars).
- [ ] **Afternoon:**
    - Implement `backend/app/main.py` with a health check endpoint.
    - Set up `backend/app/db` with Async SQLAlchemy + SQLite.
    - Create `Session` and `ChatHistory` models in `models.py`.
    - **Deliverable:** Running FastAPI server with DB connection and auto-generated tables.

### Day 2: Vector Database & Session Management
**Goal:** Implement session isolation and vector store infrastructure.
- [ ] **Morning:**
    - Set up ChromaDB client in `backend/app/rag/vector_store.py`.
    - Implement `create_session` endpoint in `backend/app/api/routers/session.py`.
    - Ensure every session generates a unique `session_id`.
- [ ] **Afternoon:**
    - Implement logic to initialize a ChromaDB collection (or verify existence).
    - Create utility functions to query ChromaDB with **metadata filtering** (`where={"session_id": "..."}`).
    - **Deliverable:** API endpoints to create sessions and a working ChromaDB connection.

## Phase 2: Core RAG Functionality (Days 3-4)

### Day 3: Asynchronous Document Ingestion
**Goal:** Handle PDF uploads, processing, and embedding without blocking the server.
- [ ] **Morning:**
    - Implement `POST /upload` endpoint in `backend/app/api/routers/documents.py`.
    - Use `UploadFile` to receive PDFs.
- [ ] **Afternoon:**
    - Implement **Async Ingestion Pipeline** in `backend/app/rag/ingestion.py`:
        - Save file temporarily (or process in memory).
        - Load PDF using `pypdf`.
        - Chunk text (RecursiveCharacterTextSplitter).
        - Generate embeddings (e.g., OpenAIEmbeddings or local HuggingFace).
        - **Critical:** Store chunks in ChromaDB with `session_id` metadata.
    - **Deliverable:** Functional upload endpoint that ingests PDFs into the vector store.

### Day 4: Retrieval & Conversational Memory
**Goal:** Connect the LLM, implement retrieval, and manage chat history.
- [ ] **Morning:**
    - Implement `backend/app/rag/chain.py` using LangChain.
    - Set up the retrieval chain:
        - Query rewriting (optional but recommended).
        - Vector search with `session_id` filter.
- [ ] **Afternoon:**
    - Implement `POST /chat` endpoint in `backend/app/api/routers/chat.py`.
    - **Memory Logic:**
        - Fetch last 5 messages from SQLite for the current session.
        - Format history for the LLM prompt.
        - Run the RAG chain.
        - Save the new User query and AI response to SQLite.
    - **Deliverable:** Full chat endpoint that answers questions based on uploaded docs and context.

## Phase 3: Frontend & Polish (Days 5-6)

### Day 5: Streamlit Frontend Implementation
**Goal:** Build the user interface.
- [ ] **Morning:**
    - Setup `frontend/app.py` and `frontend/components`.
    - Implement Session State management in Streamlit (store `session_id`).
    - Create Sidebar:
        - File uploader widget calling `POST /upload`.
        - "New Chat" button calling `POST /session`.
- [ ] **Afternoon:**
    - Create Chat Interface:
        - Display chat history from Streamlit session state (or fetch from backend).
        - Chat input box calling `POST /chat`.
        - Display "Thinking..." spinner during backend processing.
    - **Deliverable:** Functional UI connected to the backend.

### Day 6: Testing, Refinement & Documentation
**Goal:** Ensure robustness and prepare for handover.
- [ ] **Morning:**
    - **End-to-End Testing:** Verify session isolation (User A shouldn't see User B's docs).
    - **Performance Check:** Ensure PDF upload doesn't freeze the chat API (verify async).
    - Fix bugs and handle edge cases (e.g., empty documents, API failures).
- [ ] **Afternoon:**
    - Write `README.md` with setup instructions.
    - Finalize code comments and type hinting.
    - Prepare demo/walkthrough.
    - **Deliverable:** Final "Resume-Worthy" Project Codebase.
