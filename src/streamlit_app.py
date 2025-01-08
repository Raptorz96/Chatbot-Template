import streamlit as st
import os
import glob
import uuid
import sys
from langchain_community.chat_models import ChatOpenAI

# Configura il percorso della directory `src`
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Gestione delle importazioni con fallback
try:
    from src.database.chroma_db import get_chroma_client, query_knowledge
    from src.config import OPENAI_API_KEY
    from src.utils.logging import logger
    from src.utils.streaming import get_streaming_response
except ImportError:
    try:
        from database.chroma_db import get_chroma_client, query_knowledge
        from config import OPENAI_API_KEY
        from utils.logging import logger
        from utils.streaming import get_streaming_response
    except ImportError as e:
        st.error(f"Errore nell'importazione dei moduli: {str(e)}")
        st.stop()

# Genera un ID univoco per la sessione
session_id = str(uuid.uuid4())
logger.info(f"Nuova sessione avviata: {session_id}")

try:
    # Inizializza il database
    client = get_chroma_client()

    # Configura l'interfaccia Streamlit
    st.title("Chatbot Assicurativo")
    st.subheader("Chiedi informazioni sulle polizze o altri argomenti!")

    # Mostra tutte le FAQ salvate nel database
    if st.button("Mostra tutte le FAQ salvate"):
        collection_name = "assicurazioni"
        categoria = st.selectbox("Seleziona una categoria:", ["Tutte", "polizze", "auto", "sinistri", "casa", "vita"])
        try:
            collection = client.get_collection(collection_name)
            if categoria != "Tutte":
                results = [doc for doc, meta in zip(collection.get()["documents"], collection.get()["metadatas"]) if meta["categoria"] == categoria]
            else:
                results = collection.get()["documents"]

            st.write("### FAQ Filtrate:")
            for doc in results:
                st.write("- " + doc)
        except Exception as e:
            st.error(f"Errore nel recupero delle FAQ: {str(e)}")

    # Input dell'utente
    user_input = st.text_input("Inserisci la tua domanda:")

    if user_input:
        try:
            # Log della domanda
            logger.info(f"Sessione: {session_id} - Domanda: {user_input}")

            # Recupera conoscenze dal database
            knowledge = query_knowledge(client, "assicurazioni", user_input)

            # Mostra il contesto trovato
            st.write("### Contesto trovato:")
            context = knowledge["documents"][0] if knowledge["documents"] else "Nessun contesto trovato."
            st.write(context)

            # Prompt per il modello OpenAI
            prompt_text = f"Con il seguente contesto: {context}, spiega brevemente: {user_input}"

            # Modello OpenAI con streaming abilitato
            llm = ChatOpenAI(
                openai_api_key=OPENAI_API_KEY, 
                temperature=0.7,
                streaming=True,
                model_name="gpt-3.5-turbo"  # Specifichiamo il modello
            )

            # Container per la risposta streaming
            st.write("### Risposta generata:")
            response_container = st.empty()

            # Genera la risposta con streaming
            risposta = get_streaming_response(llm, prompt_text, response_container)

            # Log della risposta
            if risposta:
                logger.info(f"Sessione: {session_id} - Risposta: {risposta}")
            else:
                logger.error(f"Sessione: {session_id} - Errore nella generazione della risposta")

        except Exception as e:
            st.error(f"Si è verificato un errore: {str(e)}")
            logger.error(f"Sessione: {session_id} - Errore: {str(e)}")

    # Calcolo premi assicurativi
    st.subheader("Calcola il tuo premio assicurativo:")
    tipo_assicurazione = st.selectbox("Seleziona il tipo di assicurazione:", ["Auto", "Casa", "Vita"])
    valore_assicurato = st.number_input("Inserisci il valore del bene assicurato (€):", min_value=0)
    età = st.number_input("Inserisci la tua età:", min_value=18, max_value=100)

    if st.button("Calcola Premio"):
        # Logica per calcolare il premio
        premio_base = valore_assicurato * 0.05 if tipo_assicurazione == "Auto" else valore_assicurato * 0.03
        premio_età = premio_base * 1.2 if età < 25 else premio_base
        st.write(f"Il premio annuale stimato per la tua assicurazione è: €{premio_età:.2f}")

    # Sistema di escalation
    st.subheader("Hai bisogno di ulteriore assistenza?")
    with st.form("form_esc"):
        nome = st.text_input("Il tuo nome:")
        email = st.text_input("La tua email:")
        messaggio = st.text_area("Descrivi il tuo problema:")
        inviato = st.form_submit_button("Invia")

        if inviato:
            st.success("Richiesta inviata con successo. Ti contatteremo al più presto!")
            logger.info(f"Richiesta inviata da {nome} ({email}): {messaggio}")

except Exception as e:
    st.error(f"Errore nell'inizializzazione dell'applicazione: {str(e)}")
    logger.error(f"Errore critico: {str(e)}")