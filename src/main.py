from dotenv import load_dotenv
import os
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate

# Carica le variabili d'ambiente
load_dotenv()

# Recupera la chiave API
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    print("ERRORE: OPENAI_API_KEY non è impostata.")
    exit()

def test_chatbot():
    # Template del prompt
    prompt = PromptTemplate(
        input_variables=["argomento"],
        template="Spiega brevemente {argomento} in italiano."
    )

    # Inizializza l'LLM
    llm = OpenAI(openai_api_key=openai_key, temperature=0.7)

    # Costruisci la pipeline
    chain = prompt | llm

    # Input dell'utente
    topic = input("Inserisci un argomento da spiegare: ")

    # Esegui la catena
    print("Generando la risposta...\n")
    risposta = chain.invoke({"argomento": topic})

    # Mostra la risposta
    print(f"Risposta generata:\n{risposta}")

if __name__ == "__main__":
    test_chatbot()
