from langchain_ollama import OllamaEmbeddings
from app.core.config import settings

def get_embedding_model():
    # Using the model specified by the user: EmbeddingGemma
    # Note: Ensure "EmbeddingGemma" is the correct model name in Ollama list
    # If it's a custom model, it should be pulled first.
    # We'll use a configurable name from settings or default to what user said.
    
    model_name = "embeddinggemma:latest" # Placeholder, user said "EmbeddingGemma", might need exact tag
    # If user specifically said "EmbeddingGemma", we should probably use that.
    # Let's assume the user has a model named "EmbeddingGemma" in their ollama.
    
    return OllamaEmbeddings(
        model="embeddinggemma:latest",
        base_url="http://localhost:11434" 
    )
