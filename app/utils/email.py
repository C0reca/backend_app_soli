from email.message import EmailMessage
import aiosmtplib
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL")


async def enviar_email(destinatario: str, assunto: str, conteudo: str):
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(conteudo)

    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASS,
        start_tls=True,
    )
