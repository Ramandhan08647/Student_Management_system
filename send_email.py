import os
from dotenv import load_dotenv

from send_smtp import get_smtp_config, send_smtp_email, send_verification_email as smtp_send_verification_email

load_dotenv()

SMTP_CONFIG = get_smtp_config()


def send_email(recipient: str, subject: str, body: str, html: str = None) -> bool:
    return send_smtp_email(recipient, subject, body, html=html, config=SMTP_CONFIG)


def send_verification_email(user_email: str, username: str, otp_code: str = None) -> bool:
    if not otp_code:
        raise ValueError("OTP code is required for email verification.")
    return smtp_send_verification_email(user_email, username, otp_code, config=SMTP_CONFIG)
