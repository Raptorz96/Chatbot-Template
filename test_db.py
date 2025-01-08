from src.database.chroma_db import get_chroma_client, add_knowledge, query_knowledge, get_all_documents
from src.database.constants import INSURANCE_CATEGORIES

def test_database():
    print("Iniziando i test del database...")
    
    # 1. Test connessione al client
    try:
        client = get_chroma_client()
        print("✓ Connessione al client riuscita")
    except Exception as e:
        print(f"✗ Errore nella connessione al client: {str(e)}")
        return

    # 2. Test aggiunta documenti
    test_docs = [
        "La polizza RC Auto è obbligatoria per tutti i veicoli.",
        "L'assicurazione casa copre i danni da catastrofi naturali.",
        "La polizza vita può essere di tipo temporaneo o permanente."
    ]
    
    test_metadata = [
        {"categoria": "auto", "subcategoria": "RC Auto", "tipo": "faq"},
        {"categoria": "casa", "subcategoria": "Catastrofi Naturali", "tipo": "info"},
        {"categoria": "vita", "subcategoria": "Temporanea", "tipo": "info"}
    ]
    
    try:
        result = add_knowledge(client, "test_collection", test_docs, test_metadata)
        if result:
            print("✓ Aggiunta documenti riuscita")
        else:
            print("✗ Errore nell'aggiunta dei documenti")
    except Exception as e:
        print(f"✗ Errore nell'aggiunta dei documenti: {str(e)}")

    # 3. Test query
    try:
        results = query_knowledge(client, "test_collection", "RC Auto", categoria="auto")
        if results and results["documents"]:
            print("✓ Query riuscita")
            print(f"  Risultato: {results['documents'][0]}")
        else:
            print("✗ Query non ha prodotto risultati")
    except Exception as e:
        print(f"✗ Errore nella query: {str(e)}")

    # 4. Test recupero tutti i documenti
    try:
        all_docs = get_all_documents(client, "test_collection")
        if all_docs and all_docs["documents"]:
            print(f"✓ Recupero documenti riuscito. Trovati {len(all_docs['documents'])} documenti")
        else:
            print("✗ Nessun documento trovato")
    except Exception as e:
        print(f"✗ Errore nel recupero documenti: {str(e)}")

    # 5. Test filtro per categoria
    try:
        auto_docs = get_all_documents(client, "test_collection", categoria="auto")
        if auto_docs and auto_docs["documents"]:
            print(f"✓ Filtro categoria riuscito. Trovati {len(auto_docs['documents'])} documenti nella categoria auto")
        else:
            print("✗ Nessun documento trovato nella categoria auto")
    except Exception as e:
        print(f"✗ Errore nel filtro categoria: {str(e)}")

if __name__ == "__main__":
    test_database()