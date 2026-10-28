"""Tests du contrat typé et des vérifications du modèle de l'API."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from api import main, model


def test_charger_modele_refuse_classes_inattendues(monkeypatch, tmp_path):
    modele_path = tmp_path / "modele.joblib"
    modele_path.touch()
    monkeypatch.setattr(model, "MODELE", modele_path)
    monkeypatch.setattr(model.joblib, "load", lambda _: SimpleNamespace(classes_=["positive", "neutral"]))
    model.charger_modele.cache_clear()

    with pytest.raises(ValueError, match="Classes du modèle non prises en charge"):
        model.charger_modele()


def test_predict_refuse_texte_vide():
    with pytest.raises(ValueError, match="texte vide"):
        model.predict(" ")


def test_predict_refuse_une_etiquette_inconnue(monkeypatch):
    pipeline = SimpleNamespace(
        predict=Mock(return_value=["neutral"]),
        predict_proba=Mock(return_value=SimpleNamespace(max=lambda: 1.0)),
    )
    monkeypatch.setattr(model, "charger_modele", lambda: pipeline)

    with pytest.raises(ValueError, match="Étiquette prédite non prise en charge"):
        model.predict("Un avis")


def test_predict_route_releve_les_erreurs_http(monkeypatch):
    erreur = HTTPException(status_code=418, detail="erreur métier")
    monkeypatch.setattr(main.model, "predict", Mock(side_effect=erreur))

    with pytest.raises(HTTPException) as exc_info:
        request = SimpleNamespace(
            app=SimpleNamespace(state=SimpleNamespace(classifier=object()))
        )
        main.predict_route(main.PredictRequest(text="Un avis"), request)

    assert exc_info.value.status_code == 418
