import os
import uuid
import tempfile
import asyncio
from functools import partial
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.vector_store import vector_store
from app.rag.embeddings import get_embedding_model

def process_document(tmp_path: str, session_id: str, original_filename: str):
    """
    Synchronous function to handle CPU-bound processing.
    """
    # 2. Load PDF
    print("[BACKEND] Loading PDF...", flush=True)
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()
    print(f"[BACKEND] Loaded {len(documents)} pages.", flush=True)

    # 3. Split Text
    print("[BACKEND] Splitting text...", flush=True)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"[BACKEND] Created {len(chunks)} text chunks.", flush=True)

    # 4. Add Metadata (Session ID)
    print(f"[BACKEND] Adding metadata for session: {session_id}", flush=True)
    for chunk in chunks:
        chunk.metadata["session_id"] = session_id
        chunk.metadata["source"] = original_filename

    # 5. Embed & Store (ChromaDB)
    print("[BACKEND] Generating embeddings and storing in ChromaDB...", flush=True)
    # Get the collection directly from our vector store client
    collection = vector_store.get_collection()
    
    # Prepare data for ChromaDB
    ids = [str(uuid.uuid4()) for _ in chunks]
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    
    # We need to embed the texts using our embedding model
    embedding_model = get_embedding_model()
    embeddings = embedding_model.embed_documents(texts)
    
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print("[BACKEND] Documents stored successfully.", flush=True)
    
    return len(chunks)

async def ingest_document(file: UploadFile, session_id: str):
    # 1. Save temp file
    print(f"[BACKEND] Saving temporary file: {file.filename}", flush=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name

    try:
        # Run CPU-bound processing in a separate thread
        loop = asyncio.get_running_loop()
        chunks_processed = await loop.run_in_executor(
            None, 
            partial(process_document, tmp_path, session_id, file.filename)
        )
        
        return {
            "filename": file.filename,
            "chunks_processed": chunks_processed,
            "status": "success"
        }

    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            print("[BACKEND] Temporary file removed.", flush=True)
