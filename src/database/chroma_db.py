import chromadb
from chromadb.config import Settings

def get_chroma_client():
    """
    Inizializza il client ChromaDB in memoria.
    Returns:
        ChromaDB client instance
    """
    settings = Settings(
        anonymized_telemetry=False,
        is_persistent=False,  # Usiamo il database in memoria
        chroma_db_impl="duckdb+parquet"  # Cambiamo l'implementazione del database
    )
    
    client = chromadb.Client(settings)
    return client

def query_knowledge(client, collection_name, query_text):
    """Effettua query sul database."""
    try:
        collection = client.get_collection(collection_name)
    except:
        # Se la collezione non esiste, restituiamo un risultato vuoto
        return {"documents": ["Mi dispiace, non ho informazioni su questo argomento."], "metadatas": [{}], "distances": [0]}
    
    results = collection.query(query_texts=[query_text], n_results=1)
    return results