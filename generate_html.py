import os
import glob
import csv  # Nieuw toegevoegd voor het lezen van bijschriften

def read_captions():
    captions = {}
    try:
        with open('contents/captions.csv', 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) == 2:  # Zorg ervoor dat er voldoende waarden zijn om uit te pakken
                    filename, caption = row
                    captions[filename] = caption
    except FileNotFoundError:
        pass  # Het bestand bestaat niet, ga gewoon verder
    return captions

def generate_html():
    # Lees de bijschriften
    captions = read_captions()

    # Vind alle bestanden met de gegeven extensies
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(f'contents/fotos/*.{ext}'))

    # Sorteer de bestanden (optioneel)
    image_files.sort()

    # Begin met het genereren van HTML
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Foto Slideshow</title>
    <style>
        /* Styles... */
    </style>
</head>
<body>

<div id="slideshow">
"""

    # Voeg afbeeldingen en hun bijschriften toe aan HTML
    for image_file in image_files:
        filename = os.path.basename(image_file)
        rel_path = os.path.relpath(image_file, start='.')
        caption = captions.get(filename, '')  # Gebruik een leeg bijschrift als er geen bijschrift is
        html_content += f'    <div class="slide"><img src="{rel_path}" alt="{rel_path}"><p>{caption}</p></div>\n'

    # Voeg Javascript toe
    html_content += """
</div>

<script>
    // Javascript code...
</script>

</body>
</html>
"""

    # Schrijf de HTML naar een bestand
    with open('pagina.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

# Roep de functie aan
generate_html()
