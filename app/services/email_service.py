import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_signup_notification(user_name: str, user_email: str):
    """Send email notification to admin when a new user signs up"""
    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_SENDER
    msg["To"] = settings.ADMIN_EMAIL
    msg["Subject"] = "New User Registration - Action Required"

    body = f"""
    Hi Admin,

    A new user has signed up and requires activation:

    User Details:
    - Name: {user_name}
    - Email: {user_email}
    - Status: Inactive (Requires Activation)

    Please log into the admin dashboard to activate this user's account.

    Best regards,
    System Notification
    """

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_SENDER, settings.ADMIN_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending signup notification email: {e}")
        return False