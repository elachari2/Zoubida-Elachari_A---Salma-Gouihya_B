"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D)."""
from pathlib import Path
from unittest.mock import patch

import pytest

MODELE_PATH = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE_PATH.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    from fastapi.testclient import TestClient

    from api.main import app
    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_demarrage(monkeypatch, tmp_path):
    from fastapi.testclient import TestClient

    import api.model
    from api.main import app

    monkeypatch.setattr(api.model, "MODELE", tmp_path / "absent.joblib")
    api.model.charger_modele.cache_clear()

    with pytest.raises(FileNotFoundError):
        with TestClient(app):
            pass


def test_panne_runtime_renvoie_500():
    from fastapi.testclient import TestClient

    from api.main import app
    with TestClient(app) as client:
        with patch("api.model.predict", side_effect=RuntimeError("panne critique")):
            reponse = client.post("/predict", json={"text": "Un avis"})
            assert reponse.status_code == 500
            assert "panne critique" not in reponse.text


def test_panne_valueerror_renvoie_500():
    from fastapi.testclient import TestClient

    from api.main import app
    with TestClient(app) as client:
        with patch("api.model.predict", side_effect=ValueError("bug interne")):
            reponse = client.post("/predict", json={"text": "Un avis"})
            assert reponse.status_code == 500
            assert "bug interne" not in reponse.text