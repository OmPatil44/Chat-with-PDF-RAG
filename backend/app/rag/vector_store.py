import chromadb
from chromadb.config import Settings
from app.core.config import settings
import os

class VectorStore:
    _client = None
    _collection = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            # Ensure the directory exists
            os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
            
            cls._client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY,
                settings=Settings(allow_reset=True, anonymized_telemetry=False)
            )
        return cls._client

    @classmethod
    def get_collection(cls, collection_name: str = "research_papers"):
        if cls._collection is None:
            client = cls.get_client()
            # We will use the embedding function later when adding documents
            # For now, we just get/create the collection
            cls._collection = client.get_or_create_collection(name=collection_name)
        return cls._collection

    @classmethod
    def delete_session_documents(cls, session_id: str):
        """Delete all documents associated with a specific session_id."""
        collection = cls.get_collection()
        collection.delete(where={"session_id": session_id})

vector_store = VectorStore()
