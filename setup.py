from setuptools import setup, find_packages

setup(
    name="Chatbot-Template",
    version="0.1.0",
    packages=find_packages(),  # Rimuoviamo il where="src" per includere tutti i pacchetti
    include_package_data=True,
    install_requires=[
        # Qui dovresti elencare tutte le dipendenze del tuo progetto
        'streamlit',
        # altri pacchetti necessari...
    ],
)
