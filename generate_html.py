import os
import glob
import csv

def read_captions():
    captions = {}
    try:
        with open('contents/captions.csv', mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                filename, caption = row
                captions[filename] = caption
    except FileNotFoundError:
        print("Geen captions.csv gevonden.")
    return captions

def generate_html():
    # Lees de onderschriften uit het CSV-bestand
    captions = read_captions()

    # Vind alle bestanden met de gegeven extensies
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(f'contents/fotos/*.{ext}'))

    # Sorteer de bestanden (optioneel)
    image_files.sort()

    # Begin met het genereren van HTML
    # ... (geen wijzigingen hier)

    # Voeg afbeeldingen en onderschriften toe aan HTML
    for image_file in image_files:
        rel_path = os.path.relpath(image_file, start='.')
        filename = os.path.basename(image_file)
        caption = captions.get(filename, '')  # Haal het onderschrift op als het bestaat
        html_content += f'    <div class="slide" style="display:none;">\n'
        html_content += f'        <img src="{rel_path}" alt="{rel_path}">\n'
        html_content += f'        <p>{caption}</p>\n'
        html_content += f'    </div>\n'

    # Voeg script toe voor het wisselen van de foto's

    html_content += """
</div>

<script>
    var index = 0;
    function showNextImage() {
        var slides = document.querySelectorAll(".slide");
        slides[index].style.display = "none";
        index = (index + 1) % slides.length;
        slides[index].style.display = "block";
    }
    setInterval(showNextImage, 2000); // iedere 5 minuten een nieuwe foto om mijn moeder niet teveel te verwarren
    //setInterval(showNextImage, 300000); // iedere 5 minuten een nieuwe foto om mijn moeder niet teveel te verwarren
    // Toon de eerste afbeelding
    showNextImage();
</script>

</body>
</html>
"""

    # Schrijf de HTML naar een bestand
    with open('pagina.html', 'w') as f:
        f.write(html_content)

# Roep de functie aan
generate_html()
