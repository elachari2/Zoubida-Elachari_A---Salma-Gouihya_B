# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées
> (obligatoire) doivent contenir au moins une phrase complète.

## Besoin en une phrase (obligatoire)

Signaler au pharmacien toute ordonnance à laquelle il manque un champ obligatoire.

## Approche retenue (obligatoire)
Cocher une seule case :
- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire)

(a) Aucune ordonnance étiquetée n'existe au départ. (b) Le pharmacien doit pouvoir expliquer le refus au patient. (d) Une ordonnance validée à tort a une conséquence grave.

## Utilisateur final (obligatoire)

Le pharmacien et son assistant au comptoir.

## Données nécessaires et leur origine (obligatoire)

La liste officielle des champs obligatoires d'une ordonnance, fournie par l'ordre des pharmaciens.

## Métrique de succès et seuil (obligatoire)

Rappel d'au moins 0,95 sur les ordonnances incomplètes, mesuré sur un jeu de 200 ordonnances annotées par un pharmacien.

## Conséquence d'une erreur et validation humaine (obligatoire)

Une ordonnance incomplète non détectée peut conduire à une délivrance dangereuse. Le pharmacien valide toujours manuellement avant de refuser ou d'accepter.

## Risques éthiques ou de confidentialité (obligatoire)

Aucune donnée personnelle n'est stockée. Le système alerte, le pharmacien décide.

## Approche écartée et pourquoi (facultatif)

Le machine learning serait possible mais nécessiterait de constituer un jeu étiqueté, ce qui n'est pas justifié ici.
