from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class TextInput(BaseModel):
    """Modèle d'entrée pour l'API /predict"""
    text: str = Field(..., description="Texte à analyser pour détecter la toxicité")
    url: Optional[HttpUrl] = Field(None, description="URL source optionnelle de l'article")

class PredictionOutput(BaseModel):
    """Modèle de sortie pour la réponse /predict"""
    label: str = Field(..., description="Résultat de la prédiction ('toxique' ou 'non toxique')")
    score: float = Field(..., description="Score de confiance associé à la prédiction")
    date: datetime = Field(..., description="Date et heure de la prédiction (UTC)")
    url: Optional[HttpUrl] = Field(None, description="URL source si fournie")
