"""Chargement du modèle et prédiction, avec seuil d'abstention (TP4)."""

from functools import lru_cache
from pathlib import Path

import joblib

from src.predict import predict as predict_tp2  # ou selon l'API du TP2

MODELE = Path("models/sentiment.joblib")
SEUIL_ABSTENTION = 0.60


@lru_cache(maxsize=1)
def charger_modele():
    """Charge le modèle une seule fois (mis en cache)."""
    if not MODELE.exists():
        raise FileNotFoundError(
            f"{MODELE} absent : lancez python src/train.py"
        )
    return joblib.load(MODELE)


def predict(texte: str) -> dict:
    """Renvoie {"label": "POSITIVE"|"NEGATIVE"|"INDETERMINE", "score": float, "text": str}."""
    modele = charger_modele()
    resultat = predict_tp2(texte)
    score = float(resultat["score"])
    label = resultat["label"].upper()          # ← LA CORRECTION EST ICI
    if score < SEUIL_ABSTENTION:
        label = "INDETERMINE"
    return {"label": label, "score": score, "text": texte}