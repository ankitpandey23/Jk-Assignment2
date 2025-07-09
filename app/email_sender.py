from email.message import EmailMessage
import aiosmtplib
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Environment Variables
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.office365.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

async def send_email_async(to_email: str, subject: str, body: str):
    if not SMTP_USER or not SMTP_PASSWORD:
        raise ValueError("SMTP_USER or SMTP_PASSWORD not set in environment.")

    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        print(f"Sending email to {to_email} via {SMTP_HOST}:{SMTP_PORT}")
        response = await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
        )
        print("Email sent:", response)
    except Exception as e:
        print("Email send failed:", str(e))
        raise Exception(f"Failed to send email: {str(e)}") from e
