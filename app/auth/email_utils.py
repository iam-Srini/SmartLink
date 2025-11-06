from fastapi import BackgroundTasks
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings


def send_otp_email(
    background_tasks: BackgroundTasks,
    recipient: str,
    otp_code: str,
) -> None:
    """
    Send an OTP email asynchronously using SendGrid.
    """
    subject = "Your Verification Code"
    body = f"Hello!\n\nYour OTP code is: {otp_code}\n\nThis code expires soon, so please use it promptly."

    message = Mail(
        from_email=settings.mail_from,
        to_emails=recipient,
        subject=subject,
        html_content=f"<p>{body}</p>"
    )

    def _send():
        try:
            sg = SendGridAPIClient(settings.mail_password)
            response = sg.send(message)
            print("Status Code:", response.status_code)
        except Exception as e:
            print("Error sending email:", str(e))

    # Run SendGrid email sending in the background
    background_tasks.add_task(_send)
    
