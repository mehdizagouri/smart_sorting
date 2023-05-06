import os
import exifread
import shutil
from datetime import datetime
import helpers as HELPERS

# Chemin du dossier cible pour les photos corrompues
dossier_cible = "E:/corompu"
# Extension des fichiers à vérifier
extensions = ['.jpg', '.jpeg', '.png', '.bmp']

def delete_empty_folders(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        # delete empty subdirectories
        for dirname in dirnames:
            subdir_path = os.path.join(dirpath, dirname)
            if not os.listdir(subdir_path):
                os.rmdir(subdir_path)
                print("Deleted empty directory: ", subdir_path)

    # check if top-level directory is empty
    if not os.listdir(directory):
        os.rmdir(directory)
        print("Deleted empty top-level directory: ", directory)


def verify_corrupt_pictures(chemin):
    # Parcours récursif du dossier et des sous-dossiers
    for dossier_racine, sous_dossiers, fichiers in os.walk(chemin):
        for fichier in fichiers:
            # Vérification de l'extension du fichier
            if any(fichier.lower().endswith(ext) for ext in extensions):
                chemin_fichier = os.path.join(dossier_racine, fichier)
                # Vérification de la validité de l'image
                if not HELPERS.image_valide(chemin_fichier):
                    # Déplacement du fichier dans le dossier cible pour les photos corrompues
                    shutil.move(chemin_fichier, dossier_cible)


def trier_photos_par_derniere_modif(dossier):
    # parcourir tous les fichiers du dossier
    for fichier in os.listdir(dossier):
        chemin_fichier = os.path.join(dossier, fichier)
        
        # ignorer les sous-dossiers
        if os.path.isdir(chemin_fichier):
            continue
        
        # obtenir la date de dernière modification du fichier
        mtime = os.path.getmtime(chemin_fichier)
        date = datetime.fromtimestamp(mtime)
        
        new_folder_name = date.strftime('%Y-%m-%d')
        # Vérifier si le dossier existe déjà, sinon le créer
        if not os.path.exists(os.path.join(dossier, new_folder_name)):
            os.makedirs(os.path.join(dossier, new_folder_name))
        try:
            # Déplacer le fichier dans le nouveau dossier
            shutil.move(os.path.join(dossier, fichier), os.path.join(dossier, new_folder_name, fichier))
        except Exception as e: 
            print(e)
            continue

def trier_photos_par_date_prise_v2(chemin):
    # Parcourir tous les fichiers dans le chemin spécifié
    for filename in os.listdir(chemin):
        try:
            # Assurer que le fichier est une photo (extension en .jpg ou .png)
            if filename.lower().endswith(('.jpg', '.png')):
                    #date_str = get_date_taken(os.path.join(chemin, filename))
                    path_file = os.path.join(chemin, filename)
                    date_str = HELPERS.get_date_taken(path_file)
                    print(date_str)
                    # Convertir la chaîne en objet datetime
                    date = datetime.strptime(date_str, '%Y:%m:%d %H:%M')
                    #date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    # Créer un nouveau nom de dossier avec la date de prise de vue
                    new_folder_name = date.strftime('%Y-%m-%d')
                    # Vérifier si le dossier existe déjà, sinon le créer
                    if not os.path.exists(os.path.join(chemin, new_folder_name)):
                        os.makedirs(os.path.join(chemin, new_folder_name))
                    # Déplacer le fichier dans le nouveau dossier
                    shutil.move(os.path.join(chemin, filename), os.path.join(chemin, new_folder_name, filename))
            else:
                print(f"Le fichier {filename} n'est pas une photo (extension .jpg ou .png)")
        except Exception as e:
            print(e)
            continue

def trier_photos_par_date_prise(chemin):
    # Parcourir tous les fichiers dans le chemin spécifié
    for filename in os.listdir(chemin):
        try:
            # Assurer que le fichier est une photo (extension en .jpg ou .png)
            if filename.lower().endswith(('.jpg', '.png')):
                # Ouvrir le fichier en mode lecture binairez
                with open(os.path.join(chemin, filename), 'rb') as f:
                    # Lire les métadonnées EXIF
                    tags = exifread.process_file(f)
                # Vérifier si les métadonnées EXIF contiennent la date de prise de vue
                if 'EXIF DateTimeOriginal' in tags.keys():
                    # Extraire la date et l'heure au format chaîne de caractères
                    date_str = str(tags['EXIF DateTimeOriginal'])
                    # Convertir la chaîne en objet datetime
                    date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    #date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    # Créer un nouveau nom de dossier avec la date de prise de vue
                    new_folder_name = date.strftime('%Y-%m-%d')
                    # Vérifier si le dossier existe déjà, sinon le créer
                    if not os.path.exists(os.path.join(chemin, new_folder_name)):
                        os.makedirs(os.path.join(chemin, new_folder_name))
                    # Déplacer le fichier dans le nouveau dossier
                    shutil.move(os.path.join(chemin, filename), os.path.join(chemin, new_folder_name, filename))
                else:
                    print(f"Les métadonnées EXIF ne contiennent pas la date de prise de vue pour le fichier {filename}")
            else:
                print(f"Le fichier {filename} n'est pas une photo (extension .jpg ou .png)")
        except Exception as e:
            print(e)
            continue

def trier_dossier_par_mois(chemin):
    # Parcourir tous les fichiers dans le chemin spécifié
    for filename in os.listdir(chemin):
        lst = filename.split("-")
        print(lst[1])
        try:
            new_folder_name = lst[1]
            # Vérifier si le dossier existe déjà, sinon le créer
            if not os.path.exists(os.path.join(chemin, new_folder_name)):
                os.makedirs(os.path.join(chemin, new_folder_name))
            # Déplacer le fichier dans le nouveau dossier
            shutil.move(os.path.join(chemin, filename), os.path.join(chemin, new_folder_name, filename))
        except Exception as e:
            print(e)
            continue

def trier_dossier_par_année(chemin):
    # Parcourir tous les fichiers dans le chemin spécifié
    for filename in os.listdir(chemin):
        lst = filename.split("-")
        print(lst[0])
        try:
            new_folder_name = lst[0]
            # Vérifier si le dossier existe déjà, sinon le créer
            if not os.path.exists(os.path.join(chemin, new_folder_name)):
                os.makedirs(os.path.join(chemin, new_folder_name))
            # Déplacer le fichier dans le nouveau dossier
            shutil.move(os.path.join(chemin, filename), os.path.join(chemin, new_folder_name, filename))
        except Exception as e:
            print(e)
            continue

def trier_les_photos_doublons(folder_path):
    hashes = {}
    # boucle pour parcourir tous les fichiers
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            file_path = os.path.join(root, name)
            print(f'Traitement en cours de {file_path}')
            # vérifier si le fichier est une photo
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                # hasher le fichier
                hash = HELPERS.hashfile(file_path)
                # vérifier si le hash existe déjà dans le dictionnaire
                if hash in hashes:
                    # si oui, déplacer le fichier dans un nouveau dossier "doublons"
                    new_path = os.path.join(folder_path, "doublons", name)
                    shutil.move(file_path, new_path)
                else:
                    # si non, ajouter le hash et le chemin dans le dictionnaire
                    hashes[hash] = file_path