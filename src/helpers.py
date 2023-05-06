from PIL import Image
from PIL.ExifTags import TAGS
import hashlib

# Fonction de vérification de la validité des images
def image_valide(chemin_image):
    try:
        img = Image.open(chemin_image)
        img.verify()
        return True
    except:
        return False
    

def get_date_taken(file_path):
    try:
        image = Image.open(file_path)
        exif = image.getexif()
        for tag_id in exif:
            tag = TAGS.get(tag_id, tag_id)
            print(f'{tag} => {exif[tag_id]}')
            if tag == 'DateTimeOriginal':
                date_taken = exif[tag_id]
                return date_taken
    except:
        return None
    

# fonction pour hasher le contenu du fichier
def hashfile(path):
    with open(path, 'rb') as f:
        bytes = f.read()
        hash = hashlib.md5(bytes).hexdigest()
    return hash