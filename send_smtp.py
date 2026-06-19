import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "ramandhandumbuya01@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "ingt qhua voco plqu")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "True").lower() in ("1", "true", "yes")
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "False").lower() in ("1", "true", "yes")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "ASMRS Notifications")
SMTP_FROM_ADDRESS = os.getenv("SMTP_FROM_ADDRESS", SMTP_USER)

DEFAULT_SMTP_CONFIG: Dict[str, Optional[str]] = {
    "smtp_server": SMTP_SERVER,
    "smtp_port": SMTP_PORT,
    "smtp_user": SMTP_USER,
    "smtp_password": SMTP_PASSWORD,
    "use_tls": SMTP_USE_TLS,
    "use_ssl": SMTP_USE_SSL,
    "from_name": SMTP_FROM_NAME,
    "from_address": SMTP_FROM_ADDRESS,
}


def get_smtp_config(config: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    if config is None:
        config = DEFAULT_SMTP_CONFIG
    return {
        "smtp_server": config.get("smtp_server", SMTP_SERVER),
        "smtp_port": int(config.get("smtp_port", SMTP_PORT)),
        "smtp_user": config.get("smtp_user", SMTP_USER),
        "smtp_password": config.get("smtp_password", SMTP_PASSWORD),
        "use_tls": bool(config.get("use_tls", SMTP_USE_TLS)),
        "use_ssl": bool(config.get("use_ssl", SMTP_USE_SSL)),
        "from_name": config.get("from_name", SMTP_FROM_NAME),
        "from_address": config.get("from_address", SMTP_FROM_ADDRESS),
    }


def send_smtp_email(recipient: str, subject: str, body: str, html: Optional[str] = None, config: Optional[Dict[str, str]] = None) -> bool:
    smtp_config = get_smtp_config(config)
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = formataddr((smtp_config["from_name"], smtp_config["from_address"]))
    message["To"] = recipient
    message.set_content(body)
    if html:
        message.add_alternative(html, subtype="html")

    try:
        if smtp_config["use_ssl"]:
            with smtplib.SMTP_SSL(smtp_config["smtp_server"], smtp_config["smtp_port"]) as smtp:
                smtp.login(smtp_config["smtp_user"], smtp_config["smtp_password"])
                smtp.send_message(message)
        else:
            with smtplib.SMTP(smtp_config["smtp_server"], smtp_config["smtp_port"]) as smtp:
                if smtp_config["use_tls"]:
                    smtp.starttls()
                smtp.login(smtp_config["smtp_user"], smtp_config["smtp_password"])
                smtp.send_message(message)
        return True
    except Exception as error:
        print(f"SMTP send error: {error}")
        return False


def send_verification_email(recipient: str, username: str, otp_code: str, config: Optional[Dict[str, str]] = None) -> bool:
    subject = "ASMRS Email Verification Code"
    body = (
        f"Hello {username},\n\n"
        f"Your ASMRS verification code is: {otp_code}\n\n"
        "Enter this code in the application to complete registration.\n"
        "The code is valid for 5 minutes.\n\n"
        "Thank you,\n"
        "ASMRS Team"
    )
    return send_smtp_email(recipient, subject, body, config=config)
