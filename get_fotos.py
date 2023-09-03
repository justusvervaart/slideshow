import imaplib
import email
import os
import csv
from email.header import decode_header
from PIL import Image
import io
from pyheif import read

host = os.environ.get('EMAIL_HOST', 'imap.gmail.com')
port = int(os.environ.get('EMAIL_PORT', 993))
user = os.environ.get('EMAIL_USER', 'default_user@gmail.com')
password = os.environ.get('EMAIL_PASSWORD', 'default_password')

mail = imaplib.IMAP4_SSL(host, port)
mail.login(user, password)
mail.select('inbox')

status, messages = mail.search(None, '(UNSEEN)')
email_ids = messages[0].split()

opslag_map = 'contents/fotos'
if not os.path.exists(opslag_map):
    os.makedirs(opslag_map)

caption_map = 'contents'
caption_file_path = os.path.join(caption_map, 'captions.csv')
if not os.path.exists(caption_map):
    os.makedirs(caption_map)

with open(caption_file_path, 'a', newline='', encoding='utf-8') as caption_file:
    caption_writer = csv.writer(caption_file)
    for e_id in email_ids:
        resp, msg_data = mail.fetch(e_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        email_subject = msg["subject"]
        decoded_subject, charset = decode_header(email_subject)[0]
        if charset is not None:
            decoded_subject = decoded_subject.decode(charset)
        count = 0

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            filename = part.get_filename()
            is_heic = (filename.lower().endswith('.heic') or filename.lower().endswith('.HEIC')) if filename else False

            if not filename and (part.get_content_type() == 'image/jpeg' or part.get_content_type() == 'image/png'):
                count += 1
                filename = f"{decoded_subject}_{count}.jpg"

            if filename:
                filepath = os.path.join(opslag_map, filename)
                image_data = part.get_payload(decode=True)
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
                    filepath = filepath.lower().replace('.heic', '.jpg')
                else:
                    image = Image.open(io.BytesIO(image_data))

                image = image.convert("RGB")
                with open(filepath, 'wb') as f:
                    image.save(f, format="JPEG", optimize=True, quality=30, exif=b'')
                
                caption_writer.writerow([filepath, decoded_subject])
                print(f"Onderschrift geschreven voor {filepath}: {decoded_subject}")  # Logboekbericht
