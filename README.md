# Gestionnaire de tournoi d'échec

Ce script permet de gérer la création et le déroulement d'un tournoi d'échec. Il permet également la gestion des 
joueurs et la création de rapport pour les tournois terminés

# Fontionnalités principales

- Gestionnaire de joueurs : Offre des fonctionnalités de création, modification et suppression de joueurs dans la base de données.
- Gestionnaire de tournoi : Permet la création, la modification et la suppression de tournois. Il est également possible de lancer un tournoi créé.
- Génération de rapport : Génère des rapports basés sur les données des tournois.

## Technologies utilisées

- tinydb
- tinydb.storages
- random
- typing
- datetime

# Pré-requis

flake8      6.1.0

flake8-html 0.4.3

tinydb      4.8.0


## Installation et configuration

### Étapes d'installation
Téléchargement : Téléchargez le projet à partir de GITHUB en utilsant ce lien 
https://github.com/LeJinge/Projet4.git.

Installation des dépendances : Avant d'exécuter le programme, assurez-vous d'avoir installé 
toutes les dépendances nécessaires. Vous pouvez le faire en exécutant pip install -r requirements.txt.

### Exécution sur différents terminaux

Windows CMD :

 - Ouvrez l'invite de commande CMD.
 - Naviguez vers le répertoire du projet en utilisant la commande cd (par exemple : cd C:...\Desktop\Projet4).
 - Lancez le programme avec "python main.py".

Git Bash :

 - Ouvrez Git Bash.
 - Naviguez vers le répertoire du projet en utilisant la commande cd (par exemple : cd /c/Users/jerem/Desktop/Projet4).
 - Lancez le programme avec "python main.py".

Terminal Linux :

 - Ouvrez le terminal.
 - Naviguez vers le répertoire du projet en utilisant la commande cd.
 - Lancez le programme avec "python3 main.py".

Terminal MacOS :

 - Ouvrez le terminal.
 - Naviguez vers le répertoire du projet en utilisant la commande cd.
 - Lancez le programme avec "python3 main.py" ou "main.py", selon votre configuration.

Générer un rapport Flake8 :

Voici la commande à lancer dans le terminal afin de générer un rapport flake8 en format html sans analyser 
tous les fichiers de l'environnement. 

flake8 Controller/ Model/ View/ main.py --format=html --htmldir=rapport_flake8

