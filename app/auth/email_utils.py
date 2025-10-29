from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import BackgroundTasks
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
    VALIDATE_CERTS=settings.validate_certs
)

async def send_otp_email(background_tasks: BackgroundTasks, recipient: str, otp_code: str):
    """Send OTP email asynchronously."""
    subject = "Your Verification Code"
    body = f"Hello!\n\nYour OTP code is: {otp_code}\n\nThis code expires soon, so use it promptly."
    
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype="plain"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)