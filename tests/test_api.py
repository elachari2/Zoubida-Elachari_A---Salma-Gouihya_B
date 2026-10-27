"""Tests de l'API du TP3 (six tests)."""

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_root(client):
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (302, 307)
    assert "/docs" in r.headers["location"]


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "OK"
    assert "tfidf-logreg" in body["model"]


def test_predict_positif(client):
    r = client.post("/predict", json={"text": "Livraison rapide, produit conforme, très satisfait"})
    assert r.status_code == 200
    assert r.json()["label"] == "POSITIVE"
    assert r.json()["score"] >= 0.5


def test_predict_negatif(client):
    r = client.post("/predict", json={"text": "Produit cassé et service injoignable, à fuir"})
    assert r.status_code == 200
    assert r.json()["label"] == "NEGATIVE"


def test_predict_texte_vide_422(client):
    for texte in ("", " "):
        r = client.post("/predict", json={"text": texte})
        assert r.status_code == 422


def test_predict_champ_manquant_422(client):
    for payload in ({}, {"text": 42}):
        r = client.post("/predict", json=payload)
        assert r.status_code == 422