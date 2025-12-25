## Parser de l'offre d'emploi

# Objectif : extraire des informations structurées depuis une description d’offre d’emploi grâce à une API de génération.

# Structure du projet

[offer_parser.py] : contient la logique de parsing.

[main_offer.py] : point d’entrée FastAPI — expose une API HTTP pour analyser les offres et renvoyer un JSON structuré.

[requirements.txt] : liste des dépendances nécessaires .

# Installation
python -m pip install -r requirements.txt

# Test local du parser
# Pour tester uniquement les fonctions d’extraction (sans lancer l’API) :
python offer_parser.py 

# Lancer l’API
python main_offer.py