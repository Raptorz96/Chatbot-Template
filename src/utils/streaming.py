from typing import Any, Dict, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
import time

class StreamHandler(BaseCallbackHandler):
    """Handler per lo streaming delle risposte del modello."""
    
    def __init__(self, container):
        """Inizializza lo stream handler."""
        self.container = container
        self.text = ""
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Gestisce ogni nuovo token generato."""
        self.text += token
        self.container.markdown(self.text + "▌")
        # Aggiungiamo un piccolo ritardo tra i token
        time.sleep(0.05)  # 50 millisecondi di ritardo

def get_streaming_response(llm, prompt, container):
    """Ottiene una risposta streaming dal modello."""
    try:
        handler = StreamHandler(container)
        response = llm.invoke(prompt, config={"callbacks": [handler]})
        return response
    except Exception as e:
        container.error(f"Si è verificato un errore: {str(e)}")
        return None