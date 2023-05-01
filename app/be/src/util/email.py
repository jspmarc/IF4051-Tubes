import ssl
from smtplib import SMTP

from util.settings import get_settings

__settings = get_settings()
__smtp_server = "smtp.gmail.com"
__smtp_port = 587


def get_email_client():
    ctx = ssl.create_default_context()
    server = SMTP(__smtp_server, __smtp_port)
    try:
        server.starttls(context=ctx)
        server.login(__settings.gmail_sender_email, __settings.gmail_password)
        server.ehlo()
        yield server
    finally:
        server.quit()
