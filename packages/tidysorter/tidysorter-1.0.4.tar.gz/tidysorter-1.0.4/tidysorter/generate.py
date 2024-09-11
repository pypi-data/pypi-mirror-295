import os
import random
from constants import FILE_TYPES

def create_random_file(directory):
    # Choisir une catégorie et une extension aléatoire
    category = random.choice(list(FILE_TYPES.keys()))
    while category == 'Folders':  # S'assurer de ne pas choisir 'Folders'
        category = random.choice(list(FILE_TYPES.keys()))
    
    extension = random.choice(FILE_TYPES[category])

    # Créer un nom de fichier aléatoire
    file_name = f"random_file_{random.randint(1, 10000)}{extension}"
    
    # Chemin complet du fichier
    file_path = os.path.join(directory, file_name)
    
    # Créer le fichier vide
    with open(file_path, 'w') as f:
        pass
    
    print(f"File '{file_name}' created in '{directory}' with extension '{extension}'.")

# Exemple d'utilisation
i = 0
while i != 50:
    create_random_file("./ici")
    i = i + 1