from typing import Annotated
from fastapi import Depends

from service import EmailService
from util.settings import Settings, get_settings


class AlertService:
    _smtp_server = "smtp.gmail.com"
    _smtp_port = 587
    _initialized = False

    def __init__(
        self,
        settings: Annotated[Settings, Depends(get_settings)],
        email_service: Annotated[EmailService, Depends(EmailService.get_instance)],
    ):
        self._email_sender = settings.gmail_sender_email
        self._email_receiver = settings.notification_receiver_email
        self._email_service = email_service

    def alert(self):
        email = self._email_service
        email.send_email(content="""\
Subject: [IF4051] Test Alert system

Hello there, this message is for testing the alert system for IF4051.""")
