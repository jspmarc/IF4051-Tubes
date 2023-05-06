from __future__ import annotations
import ssl
from typing import Annotated, List
from fastapi import Depends
from smtplib import SMTP
import asyncio
from functools import lru_cache, partial
from email.mime.text import MIMEText
from email.header import Header

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

    async def send_email(
        self, subject: str, content: str, recipient: List[str] | str | None = None
    ):
        if not recipient:
            recipient = self._email_receiver
        loop = asyncio.get_event_loop()
        msg = MIMEText(content, _charset="UTF-8")
        msg["Subject"] = Header(subject, "utf-8")
        return await loop.run_in_executor(
            None,
            partial(
                self._client.sendmail,
                from_addr=self._email_sender,
                to_addrs=recipient,
                msg=msg.as_string(),
            ),
        )

    @classmethod
    @lru_cache()
    def get_instance(cls, settings: Annotated[Settings, Depends(get_settings)]):
        instance = cls.__instance

        if instance is None:
            instance = EmailService(settings)
            cls.__instance = instance

        return instance
