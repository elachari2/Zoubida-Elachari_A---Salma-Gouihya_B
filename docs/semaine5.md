# Semaine 5 : l'interface, notes du binôme


## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?
L'interface est un client. Si elle importait le modèle , elle devrait être modifiée à chaque réentraînement, et elle ne pourrait pas être déployée sur un autre serveur que l'API. En passant par l'API, la page reste indépendante du modèle.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Elle affiche INDETERMINE avec un message d'information. C'est mieux car un modèle qui n'est pas sûr (score < 0.60) risque de se tromper. Il vaut mieux passer la main à un humain que de donner une fausse réponse positive ou négative.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

Il voit un message d'erreur en haut de la page : API injoignable : lancez d'abord uvicorn api.main:app. Cela évite de faire croire à l'utilisateur que le service fonctionne alors qu'il est en panne.
