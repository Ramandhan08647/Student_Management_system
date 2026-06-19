from typing import Dict, Optional

from config import EMAIL_SETTINGS
from send_smtp import get_smtp_config, send_smtp_email, send_verification_email

class EmailService:
    def __init__(self, config: Optional[Dict] = None):
        self.config = get_smtp_config(config or EMAIL_SETTINGS)

    def send_email(self, recipient: str, subject: str, message: str, html: Optional[str] = None) -> bool:
        return send_smtp_email(recipient, subject, message, html=html, config=self.config)

    def send_verification_email(self, recipient: str, username: str, otp_code: str) -> bool:
        return send_verification_email(recipient, username, otp_code, config=self.config)
