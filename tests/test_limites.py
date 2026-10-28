"""Tests aux frontières du contrat d'entrée (TP4, étape B).

- un test paramétré de 8 cas aux frontières, qui vérifie aussi la forme du 422
- deux propriétés hypothesis :
  * tout texte non blanc de 1 à 2000 caractères reçoit 200, avec un label
    du contrat et un score entre 0 et 1 ;
  * tout texte fait de blancs reçoit 422, avec detail en liste.
"""

import pytest
from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from api.main import app


@pytest.fixture(scope="module")
def client():
    """Portée module : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    with TestClient(app) as c:
        yield c


# --- Test paramétré : 8 cas aux frontières -------------------------------

CAS_FRONTieres = [
    # (payload, statut attendu)
    ({"text": ""}, 422),
    ({"text": " "}, 422),
    ({"text": "a"}, 200),
    ({"text": "a" * 2000}, 200),
    ({"text": "a" * 2001}, 422),
    ({}, 422),
    ({"text": 42}, 422),
    ("pas-du-json", 422),  # sera envoyé via content=, pas json=
]


@pytest.mark.parametrize("payload,attendu", CAS_FRONTieres)
def test_frontieres_du_contrat(client, payload, attendu):
    if isinstance(payload, str):
        r = client.post("/predict", content=payload, headers={"content-type": "application/json"})
    else:
        r = client.post("/predict", json=payload)
    assert r.status_code == attendu, f"payload={payload!r} -> {r.status_code} au lieu de {attendu}"
    if attendu == 422:
        detail = r.json()["detail"]
        assert isinstance(detail, list), f"detail doit être une liste, reçu {type(detail)}"


# --- Propriétés hypothesis ------------------------------------------------

@given(st.text(min_size=1, max_size=2000).filter(lambda s: s.strip()))
def test_texte_non_blanc_recoit_200(texte):
    with TestClient(app) as c:
        r = c.post("/predict", json={"text": texte})
    assert r.status_code == 200, f"texte={texte!r} -> {r.status_code}"
    body = r.json()
    assert body["label"] in {"POSITIVE", "NEGATIVE", "INDETERMINE"}
    assert 0.0 <= body["score"] <= 1.0


# Caractères considérés comme blancs par str.strip() :
# Zs (séparateurs d'espace), Zl (séparateur de ligne), Zp (séparateur de paragraphe),
# et les caractères de contrôle usuels (\t, \n, \r, \v, \f) qui sont dans Cc.
BLANCS = st.text(
    alphabet=st.characters(whitelist_categories=("Zs", "Zl", "Zp"))
    | st.sampled_from(["\t", "\n", "\r", "\v", "\f"]),
    min_size=1,
    max_size=50,
)


@given(BLANCS)
def test_texte_blancs_recoit_422(texte):
    # Par construction, `texte` ne contient que des blancs : str.strip() le vide.
    assert not texte.strip(), "le générateur a produit un texte non blanc"
    with TestClient(app) as c:
        r = c.post("/predict", json={"text": texte})
    assert r.status_code == 422, f"texte={texte!r} -> {r.status_code}"
    detail = r.json()["detail"]
    assert isinstance(detail, list), f"detail doit être une liste, reçu {type(detail)}"