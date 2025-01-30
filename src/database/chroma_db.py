# Fix SQLite - DEVE essere prima di qualsiasi altro import
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb
from chromadb.config import Settings
import os

def get_chroma_client():
    """
    Inizializza il client ChromaDB.
    Returns:
        ChromaDB client instance
    """
    # Usa una directory temporanea per il database
    db_dir = os.path.join(os.getcwd(), "temp_db")
    os.makedirs(db_dir, exist_ok=True)

    try:
        # Prima prova con il client persistente
        client = chromadb.PersistentClient(
            path=db_dir,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
    except:
        # Se fallisce, usa il client in memoria
        client = chromadb.Client(
            Settings(
                anonymized_telemetry=False,
                is_persistent=False,
                allow_reset=True
            )
        )
    
    return client

def query_knowledge(client, collection_name, query_text):
    """Effettua query sul database."""
    try:
        collection = client.get_collection(collection_name)
    except:
        # Se la collezione non esiste, restituiamo un risultato vuoto
        return {"documents": ["Mi dispiace, non ho informazioni su questo argomento."], "metadatas": [{}], "distances": [0]}
    
    try:
        results = collection.query(query_texts=[query_text], n_results=1)
        return results
    except:
        return {"documents": ["Si è verificato un errore nella ricerca."], "metadatas": [{}], "distances": [0]}