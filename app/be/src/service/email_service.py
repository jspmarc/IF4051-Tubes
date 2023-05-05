from __future__ import annotations
import ssl
from typing import Annotated, List
from fastapi import Depends
from smtplib import SMTP

from util.settings import Settings, get_settings


class EmailService:
    __instance: EmailService | None = None

    def __init__(self, settings: Settings):
        """
        Treat this constructor/init as private. Never directly invoke this constructor.
        """
        if self.__instance:
            return

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        ctx = ssl.create_default_context()
        client = SMTP(smtp_server, smtp_port)
        client.starttls(context=ctx)
        client.login(settings.gmail_sender_email, settings.gmail_password)
        client.ehlo()

        self._client = client
        self._email_sender = settings.gmail_sender_email
        self._email_receiver = settings.notification_receiver_email

    def send_email(self, content: str, recipient: List[str] | str | None = None):
        if not recipient:
            recipient = self._email_receiver
        self._client.sendmail(
            from_addr=self._email_sender, to_addrs=recipient, msg=content
        )

    @classmethod
    def get_instance(cls, settings: Annotated[Settings, Depends(get_settings)]):
        instance = cls.__instance

        if instance is None:
            instance = EmailService(settings)
            cls.__instance = instance

        return instance
