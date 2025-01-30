import time
import chromadb
from chromadb.config import Settings

def get_chroma_client():
    """
    Inizializza il client ChromaDB con la nuova configurazione.
    Returns:
        ChromaDB client instance
    """
    settings = Settings(
        anonymized_telemetry=False,
        is_persistent=True
    )
    
    client = chromadb.PersistentClient(
        path="src/database/chroma_store",
        settings=settings
    )
    return client

def query_knowledge(client, collection_name, query_text):
    """Effettua query sul database."""
    collection = client.get_collection(collection_name)
    results = collection.query(query_texts=[query_text], n_results=1)
    return results