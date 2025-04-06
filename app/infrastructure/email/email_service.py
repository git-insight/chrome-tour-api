"""
Email service to send verification emails via SMTP.
This module also registers event listeners to handle email workflows.
"""

import os
import smtplib
import ssl
from email.message import EmailMessage
from app.events.user_events import event_bus
from app.models import User


class EmailService:
    """
    Provides methods to send transactional emails to users.
    """

    @staticmethod
    def send_verification_email(to_email: str, code: str):
        """
        Sends a verification email to the specified user using Gmail SMTP.

        Args:
            to_email (str): The recipient's email address.
            code (str): The verification code to send.

        Raises:
            RuntimeError: If email sending fails.
        """
        email_from = os.environ.get("EMAIL_FROM")
        email_password = os.environ.get("EMAIL_FROM_PASSWORD")

        if not email_from or not email_password:
            raise RuntimeError("Email credentials are not set in environment variables.")

        # Compose email
        subject = "Your Chrome Tour Verification Code"
        body = (
            f"Hello,\n\n"
            f"Thank you for registering on Chrome Tour.\n"
            f"Your verification code is: {code}\n\n"
            f"This code will expire in 10 minutes.\n"
            f"If you did not initiate this request, please ignore this email.\n\n"
            f"Cheers,\n"
            f"The Chrome Tour Team"
        )

        message = EmailMessage()
        message["From"] = email_from
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        # Connect to Gmail SMTP server
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email_from, email_password)
                server.send_message(message)
                print(f"[EmailService] Verification code sent to {to_email}")
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")


def register_event_handlers():
    """
    Registers asynchronous event listeners.
    To be called once during application startup.
    """

    @event_bus.on("user_registered")
    async def handle_user_registered(user: User):
        """
        Listens for 'user_registered' events and sends a verification email.

        Args:
            user (User): The newly registered user instance.
        """
        try:
            EmailService.send_verification_email(
                to_email=user.email,
                code=user.verification_code
            )
        except Exception as error:
            # You might want to log this or notify an admin
            print(f"[EmailService] Error sending email to {user.email}: {error}")
