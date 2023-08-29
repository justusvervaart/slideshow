import imaplib
import email
import os
from email.header import decode_header

# Gmail IMAP instellingen van omgevingsvariabelen
host = os.environ.get('EMAIL_HOST', 'imap.gmail.com')
port = int(os.environ.get('EMAIL_PORT', 993))
user = os.environ.get('EMAIL_USER', 'default_user@gmail.com')
password = os.environ.get('EMAIL_PASSWORD', 'default_password')

# Opslagdirectory
storage_directory = '/contents/fotos'  # Pas dit aan naar je specifieke directory

# Verbind met Gmail
mail = imaplib.IMAP4_SSL(host, port)
mail.login(user, password)
mail.select('inbox')

# Zoek ongelezen e-mails
status, messages = mail.search(None, '(UNSEEN)')
email_ids = messages[0].split()

# Loop door elke e-mail en download bijlagen en inline afbeeldingen
for e_id in email_ids:
    resp, msg_data = mail.fetch(e_id, '(RFC822)')
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    for part in msg.walk():
        content_disposition = part.get("Content-Disposition")
        content_type = part.get_content_type()

        if part.get_content_maintype() == 'multipart':
            continue
        if content_disposition is None and 'image' not in content_type:
            continue

        filename = part.get_filename()
        if not filename:
            # Als er geen bestandsnaam is, genereer een.
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                # Gebruik een standaard extensie
                ext = '.bin'
            filename = 'img-' + str(int(time.time())) + ext

        filepath = os.path.join(storage_directory, filename)
        with open(filepath, 'wb') as f:
            f.write(part.get_payload(decode=True))
