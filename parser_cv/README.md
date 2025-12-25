## Parser de CV 

# Objectif : extraire des informations structurées depuis un CV grâce à une API de génération.

# Structure du projet

[cv_parser.py] : contient la logique de parsing.

[main_cv.py] : point d’entrée FastAPI — expose une API HTTP pour analyser les offres et renvoyer un JSON structuré.

[requirements.txt] : liste des dépendances nécessaires .


# Installation 
pip install -r requirements.txt

# Test local du parser
# Pour tester uniquement les fonctions d’extraction (sans lancer l’API) :
python cv_parser.py chemin/vers/cv.pdf

# Lancer l’API
python main_cv.py
