import os
import re

# Spécifiez le dossier contenant les fichiers vidéo WebM
dossier = '/home/leo/Videos/Bloqués - Les épisodes'

# Vérifiez si le dossier existe
if not os.path.exists(dossier):
    print(f"Le dossier {dossier} n'existe pas.")
else:
    # Parcourir chaque fichier dans le dossier
    for nom_fichier in os.listdir(dossier):
        # Vérifier si le fichier est un fichier WebM
        if nom_fichier.endswith('.webm'):
            print(f"Fichier trouvé : {nom_fichier}")

            # Utiliser une expression régulière pour trouver et supprimer le numéro entier au début
            nouveau_nom = re.sub(r'^\d+\.\s*', '', nom_fichier)

            if nouveau_nom != nom_fichier:
                # Définir les chemins complets
                ancien_chemin = os.path.join(dossier, nom_fichier)
                nouveau_chemin = os.path.join(dossier, nouveau_nom)

                # Renommer le fichier
                os.rename(ancien_chemin, nouveau_chemin)
                print(f"Renommé : {nom_fichier} -> {nouveau_nom}")
            else:
                print(f"Pas de changement pour : {nom_fichier}")

    print("Renommage terminé.")