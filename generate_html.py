import os

# Definieer de locatie van de foto's en het output HTML-bestand
foto_dir = 'contents/fotos'
output_html = 'pagina.html'

# Begin HTML, CSS en JavaScript
html_start = """<!DOCTYPE html>
<html>
<head>
    <title>Foto Slideshow</title>
    <meta http-equiv="refresh" content="60"> # verander in 3600 bij productie
    <style>
        #slideshow {
            width: 100%;
            max-height: 100vh;
            overflow: hidden;
        }
        .slide {
            width: 100%;
            max-height: 100vh;
            display: none;
        }
        .slide:first-child {
            display: block;
        }
    </style>
</head>
<body>
<div id="slideshow">
"""

# Verkrijg alle fotobestanden
foto_files = [f for f in os.listdir(foto_dir) if os.path.isfile(os.path.join(foto_dir, f))]
foto_files.sort()  # Sorteer de bestanden, indien nodig

# Genereer HTML voor foto's
foto_html = ''
for foto in foto_files:
    foto_path = os.path.join('contents/fotos', foto)
    foto_html += f'    <img src="{foto_path}" class="slide">\n'

# Eindig HTML, CSS en JavaScript
html_end = """</div>
<script>
    var slideIndex = 0;
    function showSlides() {
        var i;
        var slides = document.getElementsByClassName("slide");
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";  
        }
        slideIndex++;
        if (slideIndex > slides.length) {slideIndex = 1}
        slides[slideIndex-1].style.display = "block";  
        setTimeout(showSlides, 2000);
    }
    showSlides();
</script>
</body>
</html>
"""

# Combineer alles en schrijf naar het output HTML-bestand
with open(output_html, 'w') as f:
    f.write(html_start + foto_html + html_end)

print(f"'{output_html}' is succesvol gegenereerd.")
