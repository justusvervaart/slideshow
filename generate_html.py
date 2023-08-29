import requests

def update_html(repo_user, repo_name, folder, html_file):
    url = f"https://api.github.com/repos/justusvervaart/slideshow/contents/fotos"
    
    r = requests.get(url)
    
    if r.status_code != 200:
        print(f"Fout: Kan de inhoud niet ophalen. Status code: {r.status_code}")
        return
    
    files = r.json()
    
    img_tags = []
    
    for file in files:
        if file['type'] == 'file' and (file['name'].endswith('.jpg') or file['name'].endswith('.png')):
            img_tags.append(f'<img src="{file["download_url"]}" alt="Afbeelding" />')
    
    html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Foto Slideshow</title>
    <style>
        img {{
            width: 300px;
            height: 200px;
            margin: 10px;
        }}
    </style>
</head>
<body>

<div id="slideshow">
    {''.join(img_tags)}
</div>

</body>
</html>
    '''

    with open(html_file, 'w') as f:
        f.write(html_content)

    print(f"{html_file} is bijgewerkt.")

if __name__ == '__main__':
    REPO_USER = 'justusvervaart'
    REPO_NAME = 'slideshow'
    FOLDER = 'contents/fotos'
    HTML_FILE = 'pagina.html'

    update_html(REPO_USER, REPO_NAME, FOLDER, HTML_FILE)
