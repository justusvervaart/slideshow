import imaplib
import email
import os

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

# Loop door elke e-mail en download bijlagen
for e_id in email_ids:
    resp, msg_data = mail.fetch(e_id, '(RFC822)')
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename:
            filepath = os.path.join(opslag_map, filename)
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
