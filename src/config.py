import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

# Recupera le configurazioni
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_PATH = "src/database/chroma_store"  # Percorso del database locale

# Verifica che la chiave API sia impostata
if not OPENAI_API_KEY:
    raise ValueError("ERRORE: OPENAI_API_KEY non è impostata. Controlla il file .env.")
