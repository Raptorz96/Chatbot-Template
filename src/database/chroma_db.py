import chromadb
from chromadb.config import Settings
import os
from functools import lru_cache
import hashlib
import sys

def get_chroma_client():
    """
    Inizializza il client ChromaDB.
    Returns:
        ChromaDB client instance
    """
    # Forza l'uso del client in memoria per evitare problemi di compatibilità con SQLite
    try:
        client = chromadb.Client(
            Settings(
                anonymized_telemetry=False,
                is_persistent=False,  # Usa solo memoria
                allow_reset=True
            )
        )
        print("Client ChromaDB inizializzato in memoria")
        return client
    except Exception as e:
        print(f"Errore nell'inizializzazione del client ChromaDB: {str(e)}")
        # Ultimo tentativo con il client di base
        return chromadb.Client()

def add_knowledge(client, collection_name, texts, metadati):
    """
    Aggiunge documenti al database con metadati.
    Args:
        client: ChromaDB client
        collection_name: Nome della collezione
        texts: Lista di testi da aggiungere
        metadati: Lista di metadati corrispondenti
    """
    try:
        collection = client.get_or_create_collection(collection_name)
        
        # Genera un ID univoco per ogni documento
        ids = [f"doc_{i}" for i in range(len(texts))]
        
        # Aggiungi i documenti al database
        collection.add(ids=ids, documents=texts, metadatas=metadati)
        return True
    except Exception as e:
        print(f"Errore nell'aggiunta dei documenti: {str(e)}")
        return False

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
    except Exception as e:
        print(f"Errore nella query: {str(e)}")
        return {"documents": ["Si è verificato un errore nella ricerca."], "metadatas": [{}], "distances": [0]}

@lru_cache(maxsize=100)
def cached_query_knowledge(client_id, collection_name, query_text):
    """
    Versione con cache di query_knowledge per migliorare le prestazioni.
    Usa l'ID del client invece del client stesso perché gli oggetti client non sono hashable.
    
    Args:
        client_id: ID univoco del client (usato solo per caching)
        collection_name: Nome della collezione
        query_text: Testo della query
        
    Returns:
        Risultati della query
    """
    # Recupera il client globale (non possiamo passarlo direttamente perché non è hashable)
    from src.database.chroma_db import get_chroma_client
    client = get_chroma_client()
    
    # Esegue la query normale
    return query_knowledge(client, collection_name, query_text)

def get_client_id(client):
    """
    Genera un ID univoco per il client ChromaDB.
    Necessario perché gli oggetti client non sono hashable.
    """
    # Genera un ID basato sull'oggetto
    return hashlib.md5(str(id(client)).encode()).hexdigest()