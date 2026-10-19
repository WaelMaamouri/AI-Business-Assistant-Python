import os

import ollama

from models import RapportIAResponse

MODELE = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
HOTE = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = ollama.Client(host=HOTE, timeout=120)

SYSTEME = """Tu extrais une fiche d'intervention
depuis un rapport technique en français.
Exemple : 
"Passage à la mairie de Cavaillon,
fuite réparée en 1h30."
donne client "mairie de Cavaillon",
ville "Cavaillon, duree 90.
Réponds uniquement en JSON.

Règles :
- client : nom complet de l'organisme
  ou du lieu, avec son type
  Ex: "mairie de Cavaillon",
  "médiathèque d'Orange".
- ville : comme de l'intervention.
  Elle peut faire partie du nom du 
  client : extrais-la quand même.
  Sinon "Inconnue".
- type : nature de l'intervention
  (ex : maintenance, dépannage, installation).
- priorite : "normale", "élevée" ou "urgente".
  Urgente si fuite, panne totale ou danger.
- duree : durée en minutes, nombre entier.
  Convertis les heures en minutes.
- probleme : le problème constaté, en une phrase.
- action : l'action réalisée, en une phrase.
- N'invente jamais une information absente
  du rapport.
- Si le texte n'est pas un rapport 
  d'intervention : client "Inconnu", 
  ville "Inconnue", type "Inconnue",
  duree 0."""


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