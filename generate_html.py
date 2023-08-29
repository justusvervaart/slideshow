import os

def generate_html():
    img_folder = "contents/fotos"
    img_files = [f for f in os.listdir(img_folder) if f.endswith('.jpg') or f.endswith('.png')]

    with open("pagina.html", "w") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write("<head>\n")
        f.write("    <title>Foto Slideshow</title>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("    <div id='slideshow'>\n")

        for img_file in img_files:
            f.write(f"        <img src='{img_folder}/{img_file}' alt='{img_file}'>\n")

        f.write("    </div>\n")
        f.write("</body>\n")
        f.write("</html>\n")

if __name__ == "__main__":
    generate_html()
