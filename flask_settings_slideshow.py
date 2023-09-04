from flask import Flask, request
import csv

app = Flask(Slideshow)

@app.route('/save_settings', methods=['POST'])
def save_settings():
    max_fotos = request.form.get('max_fotos', 50)
    tijdsduur_foto = request.form.get('tijdsduur_foto', 30)
    tijdstip_activatie = request.form.get('tijdstip_activatie', '9:00')
    tijdstip_uitschakelen = request.form.get('tijdstip_uitschakelen', '21:00')
    onderschrift_tonen = request.form.get('onderschrift_tonen', 'Ja')

    with open('settings.csv', 'w', newline='') as csvfile:
        fieldnames = ['Setting', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Setting': 'max_fotos', 'Value': max_fotos})
        writer.writerow({'Setting': 'tijdsduur_foto', 'Value': tijdsduur_foto})
        writer.writerow({'Setting': 'tijdstip_activatie', 'Value': tijdstip_activatie})
        writer.writerow({'Setting': 'tijdstip_uitschakelen', 'Value': tijdstip_uitschakelen})
        writer.writerow({'Setting': 'onderschrift_tonen', 'Value': onderschrift_tonen})

    return "Instellingen opgeslagen"
