import os

import ollama

from models import RapportIAResponse

MODELE = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
HOTE = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = ollama.Client(host=HOTE, timeout=120)

SYSTEME = """Tu extrais une fiche d'intervention
depuis un rapport technique en français.
Réponds uniquement en JSON.

Règles :
- client : nom exact cité dans le rapport.
- ville : ville citée, sinon "Inconnue".
- type : nature de l'intervention
  (ex : maintenance, dépannage, installation).
- priorite : "normale", "élevée" ou "urgente".
  Urgente si fuite, panne totale ou danger.
- duree : durée en minutes, nombre entier.
  Convertis les heures en minutes.
- probleme : le problème constaté, en une phrase.
- action : l'action réalisée, en une phrase.
- N'invente jamais une information absente
  du rapport."""


def analyse_avec_ollama(prompt: str) -> str:
    reponse = client.chat(
        model=MODELE,
        messages=[
            {"role": "system", "content": SYSTEME},
            {"role": "user", "content": prompt},
        ],
        format=RapportIAResponse.model_json_schema(),
        think=False,
        options={"temperature": 0},
    )
    return reponse["message"]["content"]