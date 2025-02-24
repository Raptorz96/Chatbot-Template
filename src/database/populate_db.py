from src.database.chroma_db import get_chroma_client, add_knowledge

def populate_database(client):
    """
    Popola il database con le FAQ iniziali.
    Args:
        client: ChromaDB client
    Returns:
        bool: True se l'operazione è riuscita
    """
    try:
        # Dati di esempio (FAQ)
        faq = [
            "Cos'è una polizza assicurativa?",
            "Quali sono i vantaggi di un'assicurazione auto?",
            "Come posso denunciare un sinistro?",
            "Cosa copre un'assicurazione sulla casa?",
            "Qual è la differenza tra RC auto e polizza kasko?",
            "Quali documenti sono necessari per stipulare una polizza vita?",
            "Cosa fare in caso di incidente con colpa?"
        ]

        # Metadati per ogni FAQ
        metadata = [
            {"categoria": "polizze"},
            {"categoria": "auto"},
            {"categoria": "sinistri"},
            {"categoria": "casa"},
            {"categoria": "auto"},
            {"categoria": "vita"},
            {"categoria": "sinistri"}
        ]

        # Aggiungi le FAQ al database
        add_knowledge(client, "assicurazioni", faq, metadata)
        return True
    
    except Exception as e:
        print(f"Errore durante il popolamento del database: {str(e)}")
        return False

if __name__ == "__main__":
    # Test di popolamento
    client = get_chroma_client()
    if populate_database(client):
        print("Database popolato con successo")
    else:
        print("Errore nel popolamento del database")