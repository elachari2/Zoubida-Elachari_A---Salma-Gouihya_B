"""Chargement du modèle de sentiment et prédiction."""

import os
from functools import lru_cache
from pathlib import Path
from typing import TypedDict

import joblib
from sklearn.pipeline import Pipeline

from api.schemas import Label

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"


def chemin_modele() -> Path:
    """Chemin du modèle : SENTIMENT_MODELE s'il est défini, sinon models/sentiment.joblib."""
    brut = os.environ.get("SENTIMENT_MODELE")
    if brut:
        return Path(brut)
    return MODELE


SEUIL_ABSTENTION = 0.60
ETIQUETTES_API: dict[str, Label] = {
    "positive": "POSITIVE",
    "negative": "NEGATIVE",
}


class Prediction(TypedDict):
    label: Label
    score: float
    text: str


@lru_cache(maxsize=1)
def charger_modele() -> Pipeline:
    """Charge le modèle et vérifie ses classes une seule fois par processus."""
    # ── TP6 : le chemin est résolu à l'appel, pas au chargement du module ──
    chemin = chemin_modele()
    if not chemin.exists():
        raise FileNotFoundError(
            f"modèle introuvable : {chemin} — "
            "indiquez son chemin dans la variable SENTIMENT_MODELE"
        )
    pipeline = joblib.load(chemin)
    classes = {str(etiquette) for etiquette in pipeline.classes_}
    if classes != set(ETIQUETTES_API):
        raise ValueError(f"Classes du modèle non prises en charge : {sorted(classes)}")
    return pipeline


def predict(texte: str, classifier: Pipeline | None = None) -> Prediction:
    """Renvoie la prédiction au format attendu par l'API."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = classifier if classifier is not None else charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    label = ETIQUETTES_API.get(str(etiquette))
    if label is None:
        raise ValueError(f"Étiquette prédite non prise en charge : {etiquette!r}")
    if score < SEUIL_ABSTENTION:
        label = "INDETERMINE"
    return {"label": label, "score": round(score, 4), "text": texte}