# Semaine 3 — Seuil d'incertitude

Je retiens un seuil d'incertitude de 0.60, qui envoie 117 avis sur 290 (40 %) vers un agent humain sur le jeu de démonstration, contre 0 % à 0.50 et 81 % à 0.75. Ce compromis me paraît juste car il cible les avis mitigés — où le modèle se trompe au TP2, faute d'ordre dans un sac de mots — sans noyer l'agent sous 81 % du flux, et il se déciderait en vrai avec l'équipe métier selon le volume quotidien d'avis.
