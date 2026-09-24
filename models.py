from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional

class RapportRequest(BaseModel):
    rapport: str = Field(min_length=1, max_length=5000)
    
    @field_validator("rapport")
    @classmethod
    def valider_rapport(cls, valeur):
        valeur = valeur.strip()
        
        if not valeur:
            raise ValueError("Le rapport ne peux pas être vide")
        
        return valeur
             
class RapportResponse(BaseModel):
    id: int
    client: str
    ville: str
    type: str
    priorite: Optional[Literal["normale", "élevée", "urgente"]] = None
    duree: int = Field(ge=0)
    probleme: str
    action: str    
