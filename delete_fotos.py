import os
import glob

# Definieer de directory waarin de foto's staan
storage_directory = 'contents/fotos'

# Controleer of de map bestaat
if not os.path.exists(storage_directory):
    print("De map bestaat niet.")
else:
    # Lijst alle bestanden in de map
    files = glob.glob(f"{storage_directory}/*")

    # Sorteer de bestanden op aanmaakdatum
    files.sort(key=os.path.getctime, reverse=False)
    
    print(files)  # Debugging: print de gesorteerde lijst
    
    # Behoud alleen de 30 meest recente
    for file in files[3:]:
        os.remove(file)
        print(f"Verwijderd: {file}")
