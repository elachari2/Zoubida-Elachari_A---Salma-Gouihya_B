# Fiche de cadrage : Priorisation des avis clients négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées
> (obligatoire) doivent contenir au moins une phrase complète.

## Besoin en une phrase (obligatoire)

Faire remonter les avis clients négatifs en tête de file pour répondre d'abord aux clients mécontents.

## Approche retenue (obligatoire)
Cocher une seule case :
- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire)

(a) Les étiquettes sont gratuites via la note (1 étoile = négatif). (c) Des milliers d'avis par jour justifient un modèle automatique. (d) Une erreur de classification a peu de conséquence.

## Utilisateur final (obligatoire)

L'équipe relation client qui traite les avis.

## Données nécessaires et leur origine (obligatoire)

Les avis clients existants avec leur note, extraits de la base de l'entreprise.

## Métrique de succès et seuil (obligatoire)

Rappel d'au moins 0,90 sur la classe négative, mesuré sur un jeu de 1000 avis annotés manuellement.

## Conséquence d'une erreur et validation humaine (obligatoire)

Un avis mal classé retarde légèrement la réponse, sans conséquence grave. L'équipe peut reclasser manuellement si besoin.

## Risques éthiques ou de confidentialité (obligatoire)

Les avis sont anonymisés avant traitement. Aucune donnée personnelle n'est utilisée pour l'entraînement.

## Approche écartée et pourquoi (facultatif)

Les règles métier seraient trop rigides pour la variété des avis en français.
