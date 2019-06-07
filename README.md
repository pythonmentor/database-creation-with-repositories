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
Si vous utilisez pipenv, vous pouvez définir la variable d'environnement en créant un fichier appelé .env et contenant la définition ci-dessus. Ce fichier .env doit être placé à la racine du projet, au même niveau que le fichier Pipfile.

L'exemple s'exécute ensuite avec la commande:

```
$ pipenv run python app.py
```
