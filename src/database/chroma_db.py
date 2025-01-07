# Aggiungiamo il fix per SQLite all'inizio del file
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3

import chromadb
from chromadb.config import Settings

def get_chroma_client():
    """Inizializza il client ChromaDB con la nuova configurazione."""
    client = chromadb.PersistentClient(
        path="src/database/chroma_store"  # Percorso del database
    )
    return client

def add_knowledge(client, collection_name, texts, metadati):
    """Aggiunge documenti al database con identificatori univoci."""
    collection = client.get_or_create_collection(collection_name)

    # Genera un ID univoco per ogni documento
    ids = [f"doc_{i}" for i in range(len(texts))]

    # Aggiungi i documenti al database
    collection.add(ids=ids, documents=texts, metadatas=metadati)

def query_knowledge(client, collection_name, query_text):
    """Effettua query sul database."""
    collection = client.get_collection(collection_name)
    results = collection.query(query_texts=[query_text], n_results=1)
    return results