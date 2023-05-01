from smtplib import SMTP
from typing import Annotated
from fastapi import Depends

from util.email import get_email_client
from util.settings import Settings, get_settings


class AlertService:
    _smtp_server = "smtp.gmail.com"
    _smtp_port = 587
    _initialized = False

    def __init__(
        self,
        settings: Annotated[Settings, Depends(get_settings)],
        email_client: Annotated[SMTP, Depends(get_email_client)],
    ):
        self._email_sender = settings.gmail_sender_email
        self._email_receiver = settings.notification_receiver_email
        self._email_client = email_client

    def alert(self):
        email = self._email_client
        email.sendmail(from_addr=self._email_sender, to_addrs=self._email_receiver, msg="""\
Subject: [IF4051] Test Alert system

Hello there, this message is for testing the alert system for IF4051.""")
