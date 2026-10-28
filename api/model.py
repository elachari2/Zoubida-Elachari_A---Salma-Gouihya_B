"""Chargement du modèle de sentiment et prédiction."""

from functools import lru_cache
from pathlib import Path
from typing import TypedDict

import joblib

from api.schemas import Label

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
ETIQUETTES_API: dict[str, Label] = {
    "positive": "POSITIVE",
    "negative": "NEGATIVE",
}


class Prediction(TypedDict):
    label: Label
    score: float
    text: str


@lru_cache(maxsize=1)
def charger_modele():
    """Charge le modèle et vérifie ses classes une seule fois par processus."""
    if not MODELE.exists():
        raise FileNotFoundError("models/sentiment.joblib absent : lancez python src/train.py")
    pipeline = joblib.load(MODELE)
    classes = {str(etiquette) for etiquette in pipeline.classes_}
    if classes != set(ETIQUETTES_API):
        raise ValueError(f"Classes du modèle non prises en charge : {sorted(classes)}")
    return pipeline


def predict(texte: str) -> Prediction:
    """Renvoie la prédiction au format attendu par l'API."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    label = ETIQUETTES_API.get(str(etiquette))
    if label is None:
        raise ValueError(f"Étiquette prédite non prise en charge : {etiquette!r}")
    return {"label": label, "score": round(score, 4), "text": texte}
