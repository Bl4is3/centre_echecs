# Logiciels de jeu d'échecs

Bienvenue sur l'application de jeu d'échecs basée sur le système suisse.\n
Ce jeu fonctionne en entièrement en local et peut etre utilisé sur les plateformes
Windows, Mac ou Linux.
Pour une utilisation optimale, merci de suivre le guide ci-dessous 

### Procédure pour Linux:

Créez un répertoire dédié et placez-vous dedans:

```
mkdir centre_echecs
cd /centre_echecs
```

Créez l'environnement virtuel et activez le:

```
python3 -m venv env
source env/bin/activate
```

Chargez les modules nécessaires :

```
pip install -r requirements.txt
```

Lancez l'application:

```
python3 main.py
```

### Procédure pour générer un rapport Flake8:

Positionnez-vous dans le répertoire du logiciel:

```
cd /centre_echecs
```

Tapez la commande:

```
flake8 --format=html  --htmldir=flake8_rapport
```

Pour visualiser le rapport dans votre navigateur préféré, double-cliquez sur le fichier index.html dans le répertoire flake8_rapport.
