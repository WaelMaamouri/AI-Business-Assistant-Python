import json
from fastapi import HTTPException
from models import RapportResponse
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

def charger_interventions():
    try:
        with open("data/resultats.json", "r", encoding="utf-8") as fichier:
            interventions = json.load(fichier)
    
    except FileNotFoundError:
        return []
    
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Le fichier historique contient un JSON invalide"
        )

    if not isinstance(interventions, list):
        interventions = [interventions]
    
    return interventions

def sauvegarder_interventions(interventions):
    try:
        with open("data/resultats.json", "w", encoding="utf-8") as fichier:
            json.dump(interventions, fichier, ensure_ascii=False, indent=4)

    except OSError as erreur:
        logger.error(f"Erreur lors de la sauvegarde : {erreur}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la sauvegarde de l'intervention"
        )

def generate_id(interventions):
    
    ids = [
        intervention["id"]
        for intervention in interventions
        if isinstance(intervention.get("id"), int)
    ]
    
    return max(ids, default=0) + 1

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
        return RapportResponse(**donnees)

    except ValidationError as erreur:
        logger.error(f"Données IA invalides : {erreur}")
        raise HTTPException(
            status_code=500,
            detail="Les données retournées par l'IA sont invalides"
        )
