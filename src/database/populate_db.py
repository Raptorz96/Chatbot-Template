from src.database.chroma_db import get_chroma_client, add_knowledge

# Inizializza il client del database
client = get_chroma_client()

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
print("FAQ aggiunte al database con successo.")
