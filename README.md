# Exemple d'utilisation du pattern Repository

Le présent dépôt de code illustre l'utilisation du pattern Repository pour 
structurer une couche d'accès à une base de données relationnelle à l'aide du
langage de programmation python et de la bibliothèque records.

## Installation

Pour installer les dépendances de cet exemple, vous devez au préalable vous 
assurer que la dernière version de pipenv est installé sur votre ordinateur:

```
$ pip install -U pipenv
```

Ensuite:

```
$ pipenv install 
```

Pour lancer l'exemple, créez une base de donnée sur votre serveur MySQL et
définissez une variable d'environnement appelée DATABASE_URL sur le modèle 
suivant:

```
DATABASE_URL = mysql+mysqlconnector://user:password@host:port/dbname?charset=charset
```

L'exemple s'exécute ensuite avec la commande:

```
$ pipenv run python app.py
```
