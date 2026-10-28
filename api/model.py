"""Chargement du modèle de sentiment et prédiction."""

from functools import lru_cache
from pathlib import Path

import joblib

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"


@lru_cache(maxsize=1)
def charger_modele():
    """Charge le modèle une seule fois par processus."""
    if not MODELE.exists():
        raise FileNotFoundError("models/sentiment.joblib absent : lancez python src/train.py")
    return joblib.load(MODELE)


def predict(texte: str) -> dict:
    """Renvoie la prédiction au format attendu par l'API."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": str(etiquette).upper(), "score": round(score, 4), "text": texte}
