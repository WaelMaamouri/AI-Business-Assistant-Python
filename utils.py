import json
from fastapi import HTTPException
from models import RapportIAResponse, RapportResponse
from pydantic import ValidationError
import logging

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
