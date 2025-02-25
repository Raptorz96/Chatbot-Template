import streamlit as st
import os
import glob
import uuid
import sys
import numpy as np
from langchain_community.chat_models import ChatOpenAI

# Fix per SQLite (DEVE ESSERE PRIMA DI QUALSIASI IMPORT DA CHROMADB)
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # Se fallisce, tenta di procedere con la versione di sistema
    pass

# Configura il percorso della directory `src`
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Gestione delle importazioni con fallback
try:
    from src.config import OPENAI_API_KEY
    from src.utils.logging import logger
    from src.utils.streaming import get_streaming_response, sanitize_input
except ImportError:
    try:
        from config import OPENAI_API_KEY
        from utils.logging import logger
        from utils.streaming import get_streaming_response, sanitize_input
    except ImportError as e:
        st.error(f"Errore nell'importazione dei moduli: {str(e)}")
        st.stop()

# Dizionario di traduzioni
LANGUAGES = {
    "Italiano": "it",
    "English": "en",
    "Français": "fr",
    "Español": "es",
    "Deutsch": "de"
}

TRANSLATIONS = {
    "app_title": {
        "it": "Chatbot Assicurativo",
        "en": "Insurance Chatbot",
        "fr": "Chatbot d'Assurance",
        "es": "Chatbot de Seguros",
        "de": "Versicherungs-Chatbot"
    },
    "app_subtitle": {
        "it": "Chiedi informazioni sulle polizze o altri argomenti!",
        "en": "Ask about policies or other insurance topics!",
        "fr": "Demandez des informations sur les polices ou d'autres sujets!",
        "es": "¡Pregunte sobre pólizas u otros temas de seguros!",
        "de": "Fragen Sie nach Policen oder anderen Versicherungsthemen!"
    },
    "input_placeholder": {
        "it": "Inserisci la tua domanda...",
        "en": "Enter your question...",
        "fr": "Entrez votre question...",
        "es": "Introduzca su pregunta...",
        "de": "Geben Sie Ihre Frage ein..."
    },
    "show_faqs": {
        "it": "Mostra tutte le FAQ salvate",
        "en": "Show all saved FAQs",
        "fr": "Afficher toutes les FAQ enregistrées",
        "es": "Mostrar todas las preguntas frecuentes guardadas",
        "de": "Alle gespeicherten FAQs anzeigen"
    },
    "calculator_title": {
        "it": "Calcola il tuo premio assicurativo:",
        "en": "Calculate your insurance premium:",
        "fr": "Calculez votre prime d'assurance:",
        "es": "Calcule su prima de seguro:",
        "de": "Berechnen Sie Ihre Versicherungsprämie:"
    },
    "risk_profile_title": {
        "it": "Analisi del profilo di rischio",
        "en": "Risk Profile Analysis",
        "fr": "Analyse du profil de risque",
        "es": "Análisis del perfil de riesgo",
        "de": "Risikoprofilanalyse"
    },
    "risk_profile_subtitle": {
        "it": "Analizza il tuo profilo e ricevi consigli personalizzati",
        "en": "Analyze your profile and receive personalized advice",
        "fr": "Analysez votre profil et recevez des conseils personnalisés",
        "es": "Analice su perfil y reciba consejos personalizados",
        "de": "Analysieren Sie Ihr Profil und erhalten Sie persönliche Beratung"
    },
    "support_title": {
        "it": "Hai bisogno di ulteriore assistenza?",
        "en": "Need further assistance?",
        "fr": "Besoin d'une assistance supplémentaire?",
        "es": "¿Necesita más ayuda?",
        "de": "Benötigen Sie weitere Unterstützung?"
    }
}

def t(key, lang_code):
    """Funzione per ottenere testo tradotto."""
    if key in TRANSLATIONS and lang_code in TRANSLATIONS[key]:
        return TRANSLATIONS[key][lang_code]
    return TRANSLATIONS[key]["en"] if key in TRANSLATIONS else key

# Genera un ID univoco per la sessione
session_id = str(uuid.uuid4())
logger.info(f"Nuova sessione avviata: {session_id}")

# Inizializza lo stato della sessione se non esiste
if "messages" not in st.session_state:
    st.session_state.messages = []

# Modalità fallback senza database
DATABASE_MODE = "fallback"

try:
    # Importa moduli di database solo ora, dopo il fix sqlite
    if DATABASE_MODE == "normal":
        from src.database.chroma_db import get_chroma_client, query_knowledge, cached_query_knowledge, get_client_id
        from src.database.populate_db import populate_database
        
        # Inizializza il database
        client = get_chroma_client()
        client_id = get_client_id(client)
        
        # Popola il database
        try:
            populate_database(client)
            logger.info("Database popolato con successo")
        except Exception as e:
            logger.error(f"Errore nel popolamento del database: {str(e)}")
    else:
        # Usa dati di esempio incorporati
        logger.info("Modalità fallback: utilizzo dati incorporati invece di ChromaDB")
        
        # Dati di esempio per FAQ
        FAQ_DATA = [
            {"domanda": "Cos'è una polizza assicurativa?", "categoria": "polizze"},
            {"domanda": "Quali sono i vantaggi di un'assicurazione auto?", "categoria": "auto"},
            {"domanda": "Come posso denunciare un sinistro?", "categoria": "sinistri"},
            {"domanda": "Cosa copre un'assicurazione sulla casa?", "categoria": "casa"},
            {"domanda": "Qual è la differenza tra RC auto e polizza kasko?", "categoria": "auto"},
            {"domanda": "Quali documenti sono necessari per stipulare una polizza vita?", "categoria": "vita"},
            {"domanda": "Cosa fare in caso di incidente con colpa?", "categoria": "sinistri"}
        ]
        
        # Funzione fallback per query
        def query_fallback(query_text):
            # Simulazione di ricerca semantica molto semplice
            matches = []
            for faq in FAQ_DATA:
                # Cerca se qualche parola della query è nella domanda
                if any(word.lower() in faq["domanda"].lower() for word in query_text.split()):
                    matches.append(faq)
            
            if matches:
                best_match = matches[0]["domanda"]
                categoria = matches[0]["categoria"]
                return {"documents": [best_match], "metadatas": [{"categoria": categoria}], "distances": [0]}
            else:
                return {"documents": ["Non ho trovato informazioni specifiche sulla tua domanda."], 
                        "metadatas": [{"categoria": "generale"}], 
                        "distances": [0]}
        
        # Funzione fallback con cache
        from functools import lru_cache
        
        @lru_cache(maxsize=100)
        def cached_query_fallback(query_text):
            return query_fallback(query_text)
    
    # Sidebar con impostazioni
    st.sidebar.title("Impostazioni")
    
    # Dizionario di bandiere per ogni lingua
    FLAGS = {
        "Italiano": "🇮🇹",
        "English": "🇬🇧",
        "Français": "🇫🇷",
        "Español": "🇪🇸",
        "Deutsch": "🇩🇪"
    }
    
    # Opzioni di lingua con bandiere
    language_options = [f"{FLAGS[lang]} {lang}" for lang in LANGUAGES.keys()]
    selected_language_with_flag = st.sidebar.selectbox("Lingua / Language:", language_options)
    
    # Estrai la lingua senza la bandiera
    selected_language = selected_language_with_flag.split(" ", 1)[1]
    lang_code = LANGUAGES[selected_language]
    
    # Configura l'interfaccia Streamlit
    st.title(t("app_title", lang_code))
    st.subheader(t("app_subtitle", lang_code))
    
    # Tab per diverse funzionalità
    tab1, tab2, tab3 = st.tabs(["Chat", "FAQ", "Strumenti"])
    
    with tab1:
        # Interfaccia chat
        
        # Mostra cronologia messaggi
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input utente
        user_input = sanitize_input(st.chat_input(t("input_placeholder", lang_code)))
        
        if user_input:
            # Aggiungi messaggio utente alla cronologia
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Log della domanda
            logger.info(f"Sessione: {session_id} - Domanda: {user_input}")
            
            # Recupera conoscenze dal database o fallback
            if DATABASE_MODE == "normal":
                knowledge = cached_query_knowledge(client_id, "assicurazioni", user_input)
            else:
                knowledge = cached_query_fallback(user_input)
                
            context = knowledge["documents"][0] if knowledge["documents"] else "Nessun contesto trovato."
            
            # Prompt per il modello
            prompt_text = f"Con il seguente contesto: {context}, rispondi in modo professionale a: {user_input}. Rispondi in {selected_language}."
            
            # Modello OpenAI con streaming abilitato
            llm = ChatOpenAI(
                openai_api_key=OPENAI_API_KEY, 
                temperature=0.7,
                streaming=True,
                model_name="gpt-3.5-turbo"
            )
            
            # Mostra risposta dell'assistente
            with st.chat_message("assistant"):
                response_container = st.empty()
                risposta = get_streaming_response(llm, prompt_text, response_container)
                
                # Aggiungi risposta alla cronologia
                if risposta:
                    st.session_state.messages.append({"role": "assistant", "content": risposta})
                    logger.info(f"Sessione: {session_id} - Risposta: {risposta}")
                else:
                    logger.error(f"Sessione: {session_id} - Errore nella generazione della risposta")
    
    with tab2:
        # Mostra tutte le FAQ salvate 
        if st.button(t("show_faqs", lang_code)):
            categoria = st.selectbox("Seleziona una categoria:", ["Tutte", "polizze", "auto", "sinistri", "casa", "vita"])
            
            if DATABASE_MODE == "normal":
                collection_name = "assicurazioni"
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
            else:
                # Usa i dati di esempio per le FAQ
                if categoria != "Tutte":
                    results = [faq["domanda"] for faq in FAQ_DATA if faq["categoria"] == categoria.lower()]
                else:
                    results = [faq["domanda"] for faq in FAQ_DATA]
                
                st.write("### FAQ Filtrate:")
                for doc in results:
                    st.write("- " + doc)
    
    with tab3:
        # Calcolo premi assicurativi
        st.subheader(t("calculator_title", lang_code))
        tipo_assicurazione = st.selectbox("Seleziona il tipo di assicurazione:", ["Auto", "Casa", "Vita"])
        valore_assicurato = st.number_input("Inserisci il valore del bene assicurato (€):", min_value=0)
        età = st.number_input("Inserisci la tua età:", min_value=18, max_value=100)
        
        if st.button("Calcola Premio"):
            # Logica per calcolare il premio
            premio_base = valore_assicurato * 0.05 if tipo_assicurazione == "Auto" else valore_assicurato * 0.03
            premio_età = premio_base * 1.2 if età < 25 else premio_base
            st.write(f"Il premio annuale stimato per la tua assicurazione è: €{premio_età:.2f}")
        
        # Analisi del profilo di rischio
        st.subheader(t("risk_profile_title", lang_code))
        with st.expander(t("risk_profile_subtitle", lang_code)):
            col1, col2 = st.columns(2)
            
            with col1:
                età_profilo = st.number_input("Età:", min_value=18, max_value=100, value=30, key="age_risk")
                stato_civile = st.selectbox("Stato civile:", ["Single", "Sposato/a", "Divorziato/a", "Vedovo/a"])
                figli = st.number_input("Numero di figli:", min_value=0, max_value=10, value=0)
                
            with col2:
                reddito = st.number_input("Reddito annuale (€):", min_value=0, value=30000)
                patrimonio = st.number_input("Patrimonio complessivo (€):", min_value=0, value=50000)
                immobili = st.checkbox("Possiedi immobili?")
            
            if st.button("Analizza profilo"):
                # Calcolo del punteggio di rischio
                risk_factors = [
                    età_profilo, 
                    2 if stato_civile == "Sposato/a" else 1, 
                    min(figli * 1.5, 10),
                    min(reddito / 10000, 10),
                    min(patrimonio / 20000, 10),
                    5 if immobili else 0
                ]
                
                risk_score = sum(risk_factors) / len(risk_factors)
                normalized_score = (risk_score / 10) * 100
                
                # Visualizzazione risultati
                st.write(f"### Punteggio di rischio: {normalized_score:.1f}/100")
                
                st.progress(normalized_score/100)
                
                # Raccomandazioni
                st.write("### Polizze consigliate:")
                if normalized_score > 70:
                    st.write("🛡️ **Piano di protezione completo**")
                    st.write("- Polizza vita con capitale elevato")
                    st.write("- Polizza sanitaria premium")
                    st.write("- Protezione del patrimonio")
                elif normalized_score > 40:
                    st.write("🛡️ **Piano di protezione standard**")
                    st.write("- Polizza vita base")
                    st.write("- Polizza sanitaria standard")
                    st.write("- Protezione responsabilità civile")
                else:
                    st.write("🛡️ **Piano di protezione essenziale**")
                    st.write("- Polizza infortuni")
                    st.write("- Assicurazione auto/moto")
                    st.write("- Protezione casa base")
    
    # Sistema di escalation
    st.subheader(t("support_title", lang_code))
    with st.form("form_esc"):
        nome = st.text_input("Il tuo nome:")
        email = st.text_input("La tua email:")
        messaggio = st.text_area("Descrivi il tuo problema:")
        inviato = st.form_submit_button("Invia")
        
        if inviato:
            nome = sanitize_input(nome)
            email = sanitize_input(email)
            messaggio = sanitize_input(messaggio)
            st.success("Richiesta inviata con successo. Ti contatteremo al più presto!")
            logger.info(f"Richiesta inviata da {nome} ({email}): {messaggio}")

except Exception as e:
    st.error(f"Errore nell'inizializzazione dell'applicazione: {str(e)}")
    logger.error(f"Errore critico: {str(e)}")