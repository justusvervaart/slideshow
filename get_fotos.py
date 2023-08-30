import imaplib
import email
import os
import csv  # Nieuw geïmporteerd voor het schrijven van CSV-bestanden
from email.header import decode_header
from PIL import Image
import io
from pyheif import read  # Nieuw toegevoegd

# Gmail IMAP instellingen van omgevingsvariabelen
host = os.environ.get('EMAIL_HOST', 'imap.gmail.com')
port = int(os.environ.get('EMAIL_PORT', 993))
user = os.environ.get('EMAIL_USER', 'default_user@gmail.com')
password = os.environ.get('EMAIL_PASSWORD', 'default_password')

# Verbind met Gmail
mail = imaplib.IMAP4_SSL(host, port)
mail.login(user, password)
mail.select('inbox')

# Zoek ongelezen e-mails
status, messages = mail.search(None, '(UNSEEN)')
email_ids = messages[0].split()

# Zorg ervoor dat de opslagmap bestaat
opslag_map = 'contents/fotos'
if not os.path.exists(opslag_map):
    os.makedirs(opslag_map)

# Open het tekstbestand om het onderwerp en de bestandsnaam op te slaan
caption_file_path = 'contents/captions.csv'
with open(caption_file_path, 'a', newline='', encoding='utf-8') as caption_file:
    caption_writer = csv.writer(caption_file)

    # Loop door elke e-mail en download bijlagen
    for e_id in email_ids:
        resp, msg_data = mail.fetch(e_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        email_subject = msg["subject"]
        decoded_subject, charset = decode_header(email_subject)[0]
        if charset is not None:
            decoded_subject = decoded_subject.decode(charset)
        count = 0  # Teller voor inline afbeeldingen

        for part in msg.walk():
            content_disposition = part.get("Content-Disposition", None)
            content_type = part.get_content_type()
            if part.get_content_maintype() == 'multipart':
                continue

            filename = part.get_filename()

            is_heic = (filename.lower().endswith('.heic') or filename.lower().endswith('.HEIC')) if filename else False

            if not filename:
                if content_type == 'image/jpeg' or content_type == 'image/png':
                    count += 1
                    filename = f"{decoded_subject}_{count}.jpg"
            
            if filename:
                filepath = os.path.join(opslag_map, filename)
                image_data = part.get_payload(decode=True)
                
                # HEIC naar JPG conversie
                if is_heic:
                    heif_file = read(io.BytesIO(image_data))
                    image = Image.frombytes(
                        heif_file.mode,
                        heif_file.size,
                        heif_file.data,
                        "raw",
                        heif_file.mode,
                        heif_file.stride,
                    )
                    filepath = filepath.lower().replace(".heic", ".jpg")
                else:
                    image = Image.open(io.BytesIO(image_data))
                
                image = image.convert("RGB")  # Converteer naar RGB als het een andere kleurmodus is
                
                # Sla de afbeelding op
                with open(filepath, 'wb') as f:
                    image.save(f, format="JPEG", optimize=True, quality=20)  # Pas de kwaliteitsparameter aan naar wens
                
                # Schrijf het onderwerp en de bestandsnaam naar het tekstbestand
                caption_writer.writerow([filepath, decoded_subject])
