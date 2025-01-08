import time
import chromadb
from chromadb.config import Settings
from .constants import INSURANCE_CATEGORIES, DEFAULT_METADATA

def get_chroma_client():
    """
    Inizializza il client ChromaDB con la nuova configurazione.
    Returns:
        ChromaDB client instance
    """
    client = chromadb.PersistentClient(
        path="src/database/chroma_store"
    )
    return client

def validate_metadata(metadata):
    """
    Valida i metadati del documento.
    
    Args:
        metadata (dict): Metadati da validare
    
    Raises:
        ValueError: Se i metadati non sono validi
    """
    if metadata.get("categoria") and metadata["categoria"] != "Tutte":
        if metadata["categoria"] not in INSURANCE_CATEGORIES:
            raise ValueError(f"Categoria non valida: {metadata['categoria']}")
        
        if metadata.get("subcategoria"):
            valid_subcategories = INSURANCE_CATEGORIES[metadata["categoria"]]["subcategories"]
            if metadata["subcategoria"] not in valid_subcategories:
                raise ValueError(f"Sottocategoria non valida per {metadata['categoria']}")

def add_knowledge(client, collection_name, texts, metadati):
    """
    Aggiunge documenti al database con metadati strutturati.
    
    Args:
        client: ChromaDB client
        collection_name (str): Nome della collezione
        texts (list): Lista di documenti da inserire
        metadati (list): Lista di metadati per ogni documento
    
    Returns:
        bool: True se l'operazione è riuscita
    """
    try:
        collection = client.get_or_create_collection(collection_name)
        
        # Validazione e completamento dei metadati
        for i, metadata in enumerate(metadati):
            # Merge con i metadati di default
            complete_metadata = DEFAULT_METADATA.copy()
            complete_metadata.update(metadata)
            complete_metadata["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Validazione
            validate_metadata(complete_metadata)
            
            # Aggiorna i metadati con la versione completa
            metadati[i] = complete_metadata
        
        # Genera ID univoci con timestamp
        ids = [f"doc_{i}_{int(time.time())}" for i in range(len(texts))]
        
        # Aggiungi i documenti al database
        collection.add(ids=ids, documents=texts, metadatas=metadati)
        return True
        
    except Exception as e:
        print(f"Errore nell'aggiunta dei documenti: {str(e)}")
        return False

def query_knowledge(client, collection_name, query_text, categoria=None, n_results=3):
    """
    Effettua query sul database con filtro opzionale per categoria.
    
    Args:
        client: ChromaDB client
        collection_name (str): Nome della collezione
        query_text (str): Testo della query
        categoria (str, optional): Categoria per filtrare i risultati
        n_results (int, optional): Numero di risultati da restituire
    
    Returns:
        dict: Risultati della query
    """
    try:
        collection = client.get_collection(collection_name)
        
        # Prepara il filtro se è specificata una categoria
        where = {"categoria": categoria} if categoria and categoria != "Tutte" else None
        
        # Esegui la query
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where if where else None
        )
        return results
        
    except Exception as e:
        print(f"Errore nella query del database: {str(e)}")
        return {"documents": [], "metadatas": [], "distances": []}

def get_all_documents(client, collection_name, categoria=None):
    """
    Recupera tutti i documenti di una collezione, opzionalmente filtrati per categoria.
    
    Args:
        client: ChromaDB client
        collection_name (str): Nome della collezione
        categoria (str, optional): Categoria per filtrare i risultati
    
    Returns:
        dict: Tutti i documenti nella collezione
    """
    try:
        collection = client.get_collection(collection_name)
        
        if categoria and categoria != "Tutte":
            return collection.get(where={"categoria": categoria})
        else:
            return collection.get()
            
    except Exception as e:
        print(f"Errore nel recupero dei documenti: {str(e)}")
        return {"documents": [], "metadatas": [], "ids": []}