# Semaine 4 — tests approfondis et qualité

## 1. Mesures de départ (T21)

- **pytest** : 71 passed, 4 xfailed, 0 failed
- **Couverture** : TOTAL 89 %
  - `api/main.py` : 78 % — lignes manquantes 36-39, 43-45
  - `api/model.py` : 95 % — ligne manquante 18
  - `api/schemas.py` : 100 %
- **ruff** : 11 remarques
  - F841 ×1 : `api/model.py:26` (`modele` assigné mais inutilisé)
  - F401 ×1 : `src/evaluate.py:13` (`ConfusionMatrixDisplay` importé, inutilisé)
  - B905 ×2 : `src/evaluate.py:44,52` (`zip()` sans `strict=`)
  - E741 ×6 : `tests/test_cadrage.py:51`, `tests/test_environment.py:38,39`, `ui/helpers.py:47,48,49`
  - I001 ×1 : `ui/app.py:6` (imports non triés)
- **mypy** : `Success: no issues found in 3 source files.`

## 2. Contrat d'entrée (T22, T23)
- `field_validator` dans `api/schemas.py` : refuse un texte vide une fois ses blancs retirés, avec la même règle que `predict()` du TP2.
- `tests/test_limites.py` : test paramétré de 8 cas aux frontières + 2 propriétés hypothesis.
- Résultat : 10 passed × 3.

## 3. Abstention (T24)
- `SEUIL_ABSTENTION = 0.60` dans `api/model.py`.
- Texte inventé dans /docs → `INDETERMINE`, score 0,5162 (score toujours renvoyé).

## 4. Jeu d'or (T25)
- 20 avis, 5 difficiles (négation, ironie).
- `python src/bilan_jeu_or.py` → <copier-coller la sortie>
- 4 erreurs franches déclarées dans `erreur_connue` :
  - ligne 4 : ironie non détectée
  - ligne 10 : vocabulaire négatif mal pondéré
  - ligne 12 : double négation mal gérée
  - ligne 19 : adjectif décevant mal pondéré
- `python -m pytest -q tests/test_jeu_or.py` → 17 passed, 4 xfailed.