"""Contrat d'entrée et de sortie de l'API."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]

MAX_LEN = 2000


class PredictRequest(BaseModel):
    text: str = Field(..., max_length=MAX_LEN, description="Avis client à analyser")

    @field_validator("text")
    @classmethod
    def text_non_vide(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("texte vide")
        return v


class PredictResponse(BaseModel):
    label: Label
    score: float
    text: str


class HealthResponse(BaseModel):
    status: str
    model: str