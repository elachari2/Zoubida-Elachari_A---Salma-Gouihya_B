# Compte rendu — Salma Gouihya (Membre B)

Dépôt : https://github.com/elachari2/Zoubida-Elachari_A---Salma-Gouihya_B

Mon rôle dans le binôme a porté sur l'analyse des erreurs du modèle, la mesure
du seuil d'incertitude, la documentation, et les étapes D et E du TP2 ainsi que
les étapes C et D du TP3.



# 1. Le besoin et le cadrage

L'équipe relation client reçoit des milliers d'avis chaque jour et les traite
dans l'ordre d'arrivée. Le but du projet est de faire remonter les avis négatifs
en tête de file, pour répondre en priorité aux clients mécontents.

Au TP1, nous avons cadré trois cas avec la grille de critères (a) à (d) : les
ordonnances incomplètes pour la pharmacie, le règlement intérieur et les avis
clients négatifs. C'est ce dernier cas qui est devenu notre fil rouge. Pour le
cas des avis, la justification que nous avons retenue est la suivante. D'abord,
les notes 1 ou 2 étoiles fournissent une étiquette gratuite, donc on a bien des
données étiquetées. Ensuite, la vérifiabilité n'est pas critique, l'utilisateur
final est un agent interne. Le coût par requête reste modeste car on parle de
milliers d'avis par jour, un modèle linéaire suffit largement. Enfin, la
conséquence d'une erreur est faible, un avis mal classé se requalifie d'un clic.
C'est ce cadrage qui a fixé notre métrique : le rappel sur la classe négative,
avec un seuil d'acceptation à 0,85 de F1 macro.



# 2. L'architecture du dépôt

Le dépôt contient sept dossiers : data, models, app, ui, tests, scripts et docs.
Les dossiers encore vides contiennent un fichier .gitkeep, parce que Git ne
versionne pas les dossiers, seulement les fichiers. Sans ce témoin, un dossier
vide disparaîtrait au clone et la structure ne serait pas la même sur les deux
postes.

La règle la plus importante que j'ai retenue est la suivante : tout ce qui se
régénère par une commande n'entre pas dans Git. L'environnement virtuel est
exclu, parce qu'on le reconstruit avec pip install -r requirements.txt. Le jeu
de démonstration demo_reviews.csv est exclu, parce qu'on le reconstruit avec
python src/make_demo.py. Le modèle sentiment.joblib est exclu aussi, parce qu'on
le reconstruit avec python src/train.py --allocine. En revanche, le fichier
metrics.json est versionné. Il faut réentraîner pour le reconstruire, et il
porte la mesure qui sert de porte de validation dans l'intégration continue.
C'est ce qui permet à la CI de vérifier la qualité du modèle sans jamais
télécharger l'artefact lourd.



# 3. Le modèle

Le pipeline est un TF-IDF avec des bigrammes, suivi d'une régression logistique.
Le vecteur et le modèle voyagent dans un seul objet Pipeline, ce qui garantit
que la transformation appliquée en production est exactement celle de
l'entraînement. Le découpage entre entraînement et test se fait avant la
vectorisation, avec une graine fixée à 42 et une stratification sur l'étiquette.
Si on faisait l'inverse, les mots du jeu de test influenceraient l'apprentissage
du vocabulaire : le score monterait, mais il serait faux. C'est la fuite de
données, l'erreur la plus fréquente et la plus difficile à repérer après coup.

Nous avons utilisé deux jeux de données. Le jeu de démonstration contient 290
avis et donne un F1 macro de 0,879, avec un rappel de 0,931 sur la classe
négative. Le jeu Allociné contient 20 000 avis et donne un F1 macro de 0,920,
avec un rappel de 0,911 sur la classe négative. Le modèle n'a pas changé entre
les deux, ce sont les données. Le vocabulaire passe de 316 à 149 529 termes, et
surtout la mesure devient enfin crédible, calculée sur 4 000 avis de test au
lieu de 58. Avec 58 avis, une erreur de plus déplace le score de deux points,
donc on ne peut rien conclure d'un tel échantillon.



# 4. L'analyse des erreurs

Sur les 58 avis du jeu de test de la démonstration, le modèle se trompe sept
fois. Dans la matrice de confusion, cela donne 27 vrais négatifs, 2 faux
positifs, 5 faux négatifs et 24 vrais positifs. En lisant par ligne, sur 29 avis
réellement négatifs, 27 ont été reconnus et 2 pris pour des positifs. Sur 29
avis réellement positifs, 24 ont été reconnus et 5 pris pour des négatifs.

Ce qui compte pour notre fiche de cadrage, c'est le rappel sur la classe
négative. Les deux faux positifs sont des clients mécontents traités en retard,
c'est le cas grave. Les cinq faux négatifs sont des avis positifs remontés pour
rien, sans conséquence réelle. L'exactitude de 0,879 ne dit rien de tout cela :
une métrique unique cache toujours la question qu'on se pose vraiment.

Toutes ces erreurs sont sur des avis mitigés. Un exemple concret, tiré de nos
données : « Service impeccable et livraison en avance sur le papier, sauf que
ensuite produit cassé à l'arrivée. » L'étiquette réelle est négative, mais le
modèle prédit positif. La raison est simple. Le modèle compte des mots positifs
et des mots négatifs, puis tranche en faveur du camp le plus fourni. Il ne voit
pas le retournement, parce qu'un sac de mots n'a pas d'ordre. « Bon au début,
mauvais ensuite » et « mauvais au début, bon ensuite » lui donnent exactement le
même vecteur. C'est la limite annoncée en cours, et nous l'avons mesurée au lieu
de la croire sur parole. Pour aller plus loin, il faudrait des représentations
qui tiennent compte de l'ordre, comme les embeddings ou un modèle séquentiel.



# 5. Le seuil d'incertitude

Dans l'interface Streamlit, on ajoute un verdict « à vérifier » quand la
confiance du modèle tombe sous une constante appelée SEUIL_INCERTITUDE. Cette
constante vit dans ui/helpers.py, séparée de app.py, pour être testable sans
lancer Streamlit.

Nous avons mesuré l'effet du seuil sur le jeu de démonstration, qui contient
290 avis. Avec un seuil à 0,50, aucun avis n'est marqué incertain. Avec un seuil
à 0,60, 117 avis sur 290 sont marqués à vérifier, soit 40 pour cent. Avec un
seuil à 0,75, 234 avis sont marqués, soit 81 pour cent. Ce résultat peut
surprendre au premier abord, mais il est cohérent : le score retourné par
predict() est la probabilité maximale entre les deux classes, donc toujours
supérieur ou égal à 0,5. Avec un seuil strictement inférieur à 0,50, aucun avis
ne peut être incertain. La zone d'incertitude utile commence juste au-dessus.

Nous retenons le seuil de 0,60, qui envoie 117 avis vers un agent. Ce chiffre
élevé s'explique par la composition du jeu : 100 avis mitigés et 30 avis neutres,
soit 130 avis ambigus pour un sac de mots. À 0,75, on noierait l'agent sous 81
pour cent du flux et l'automatisation perdrait tout son intérêt. À 0,50, on
laisserait le modèle trancher des cas qu'il ne maîtrise pas. Ce curseur ne se
règle pas dans le code, il se décide avec l'équipe métier, et il découle
directement de la fiche de cadrage du cas 3 : un avis mal classé se requalifie
d'un clic, donc mieux vaut marquer « à vérifier » que trancher à tort.



# 6. Échecs et recul

Trois échecs ont marqué ma progression.

Le premier est l'absence de pyarrow au TP2. Le jeu Allociné est distribué au
format Parquet, et pandas a besoin de pyarrow pour le lire. Notre installation
initiale s'était limitée à pandas, scikit-learn et pytest, ce qui suffisait pour
la démo CSV mais pas pour Allociné. J'ai corrigé avec un simple pip install
pyarrow.

Le deuxième est un conflit de dépendances. En tentant d'installer tout le
fichier requirements.txt, pip a détecté un conflit entre mlflow et pyarrow. La
version de mlflow que nous avions exigeait pyarrow inférieur à 18, alors que le
fichier demandait pyarrow 21. Ce conflit venait du kit lui-même. J'ai décidé
d'installer uniquement les paquets nécessaires au TP2, et de repousser mlflow,
streamlit et dvc aux semaines suivantes.

Le troisième est une erreur sur scikit-learn. Le fichier sentiment.joblib avait
été produit par scikit-learn 1.9.1, mais notre environnement virtuel utilisait
la version 1.5.2. Les modèles sérialisés ne sont pas portables entre versions
majeures : le chargement plantait avec un AttributeError sur l'attribut
multi_class. J'ai supprimé le fichier et régénéré le modèle localement avec
python src/train.py --allocine, ce qui a tout remis d'aplomb.

Ce que je retiens de ces trois échecs, c'est qu'un modèle n'est pas un objet
isolé. Il est lié à la version de la librairie qui l'a produit. C'est exactement
pourquoi le fichier .joblib n'est jamais versionné : il se régénère localement
sur chaque poste. Ce que Git transporte, c'est la recette, c'est-à-dire le code,
et la mesure, c'est-à-dire metrics.json, pas l'artefact. Un compte rendu sans
échec ne serait pas crédible, et ce sont ces trois blocages qui m'ont le plus
appris sur l'écart entre un notebook et un produit.



# 7. Ce que j'ai fait concrètement

Au TP1, j'ai cloné le dépôt créé par Zoubida, fait le setup, rédigé la fiche de
cadrage 2 sur le règlement intérieur, et complété le README avec mon nom dans
le tableau du binôme.

Au TP2, j'ai lancé evaluate.py, analysé les sept erreurs, rédigé le fichier
docs/semaine2.md et poussé la version Allociné du modèle et de ses métriques.

Au TP3, j'ai complété l'onglet « un fichier CSV » dans ui/app.py, mesuré les
trois seuils d'incertitude, rédigé docs/semaine3.md et posé l'étiquette finale
sur le dépôt.

Les commits sont signés par les deux noms configurés au TP1. Le test
test_git_history.py le vérifie : deux auteurs distincts, ce qui est la condition
du contrôle T5.



# 8. Conclusion

Ce module m'a fait vivre l'écart entre un notebook et un produit. Un modèle
linéaire de vingt lignes classe déjà correctement des avis, mais ce qui prend
vraiment du temps, c'est de le rendre reproductible, testé, surveillé,
utilisable par quelqu'un d'autre, et redéployable après un réentraînement.

Les trois artefacts que sont le code, les données et le modèle n'ont pas le
même destin. Le code et la mesure voyagent dans Git. Le venv, le jeu de
démonstration et le modèle se reconstruisent en une commande. C'est ce principe
qui porte tout le raisonnement MLOps du semestre, et c'est ce que nous avons
appliqué concrètement.

Enfin, l'analyse des erreurs m'a montré qu'un score global ne dit rien. C'est la
lecture de la matrice de confusion, croisée avec la fiche de cadrage, qui dit si
le système trompe là où ça compte. Un rappel de 0,93 sur la classe négative vaut
mieux qu'une exactitude de 0,95, quand l'enjeu est de ne pas rater un client
mécontent.
