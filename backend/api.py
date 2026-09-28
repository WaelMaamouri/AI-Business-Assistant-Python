from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from typing import List
from ai_service import analyse_avec_ollama
from repository import (
    enregistrer_intervention, 
    lister_interventions, 
    trouver_intervention
    )
from utils import (
    convertir_en_json,
    valider_donnees_ia)
from models import (
    RapportRequest,
    RapportResponse
)
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
    
@app.get("/health")
def health():
    return{
        "status": "ok"
    }
    
@app.get("/")
def accueil():
    return {"message" : "Api Assistant IA opérationnelle"}

@app.post(
    "/analyser",
    response_model=RapportResponse,
    responses={
        500:{
            "description": "Erreur lors du traitement du rapport"
        }
    }
)      
def analyser_rapport(demande: RapportRequest):
    
    contenu = demande.rapport
    
    logger.info("Début de l'analyse du rapport")
    
    prompt = f"""
Retourne uniquement un objet JSON valide avec exactement les champs suivants:
client
ville
type
priorite
duree: nombre entier représentant le nombre des minutes
probleme
action

Pour le champ priorite, choisis obligatoirement une seule valeur parmi :
"normale", "élevée", "urgente".

Règles :
- normale : problème avec peu ou pas d'impact sur l'activité
- élevée : problème avec un impact important sur l'activité
- urgente : problème critique, dangereux ou bloquant l'activité

Choisis la priorité en fonction du contexte du rapport.

Retourne uniquement le JSON, sans explication.

Rapport :

{contenu}
"""
    try: 
        contenu_ia = analyse_avec_ollama(prompt)
        
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la communication avec Ollama"
        )
    
    donnees = convertir_en_json(contenu_ia)
    
    rapport_ia = valider_donnees_ia(donnees)
    
    id = enregistrer_intervention(rapport_ia.model_dump())
    
    rapport = RapportResponse(
        id=id,
        **rapport_ia.model_dump()
    )
    
    logger.info(f"Analyse terminée - intervention ID : {id}")
    
    return rapport

@app.get("/historique", response_model=List[RapportResponse])
def historique():
    
    interventions = lister_interventions()
        
    return interventions

@app.get(
    "/historique/{id}",
    response_model=RapportResponse,
    responses={
        404: {
            "description" : "Intervention introuvable"
        }
    }
    )
def historique_intervention(id: int):
    
    intervention = trouver_intervention(id)
        
    if intervention is None:    
        raise HTTPException(
            status_code=404,
            detail="Intervention introuvable"
        )
    
    return intervention
