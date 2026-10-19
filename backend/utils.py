import json
from fastapi import HTTPException
from models import RapportIAResponse
from pydantic import ValidationError
import logging
import re

logger = logging.getLogger(__name__)

def convertir_en_json(contenu_ia):
    try:
        return json.loads(contenu_ia)
    
    except json.JSONDecodeError:
        logger.error("L'IA n'a pas retourné un JSON valide")
        raise HTTPException(
            status_code=500,
            detail="L'IA n'a pas retourné un JSON valide"
        )
        
def valider_donnees_ia(donnees):
    try:
        return RapportIAResponse(**donnees)

    except ValidationError as erreur:
        logger.error(f"Données IA invalides : {erreur}")
        raise HTTPException(
            status_code=500,
            detail="Les données retournées par l'IA sont invalides"
        )
        
def est_inconnu(valeur):
    return valeur.strip().lower().startswith("inconn")

def ville_depuis_client(client):
    motif = (
        r"\b(?:d'|de |du |des )"
        r"([A-ZÉÈ][\w'-]+(?: [A-ZÉÈ][\w'-]+)*)"
    )
    trouve = re.search(motif, client)
    return trouve.group(1) if trouve else ""

def corriger_ville(rapport_ia, texte):
    ville = rapport_ia.ville.strip()
    if est_inconnu(ville):
        ville = ville_depuis_client(rapport_ia.client)
    if ville and ville.lower() not in texte.lower():
        ville = ""
    rapport_ia.ville = ville or "Inconnue"
    return rapport_ia

def verifier_expoloitable(rapport_ia):
    if (
        rapport_ia.duree == 0
        and est_inconnu(rapport_ia.client)
        and est_inconnu(rapport_ia.type)
    ):
        raise HTTPException(
            status_code=422,
            detail="Ce texte ne ressemble pas "
            "à un rapport d'intervention",
        )
