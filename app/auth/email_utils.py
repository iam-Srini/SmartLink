from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.core.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
)


def send_otp_email(
    background_tasks: BackgroundTasks,
    recipient: str,
    otp_code: str,
) -> None:
    """
    Send an OTP email asynchronously using FastMail.
    """
    subject = "Your Verification Code"
    body = (
        "Hello!\n\n"
        f"Your OTP code is: {otp_code}\n\n"
        "This code expires soon, so please use it promptly."
    )

    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype="plain",
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
