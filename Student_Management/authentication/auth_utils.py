import bcrypt
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional

from config import PASSWORD_SALT_ROUNDS, OTP_EXPIRY_SECONDS

class AuthUtils:
    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(PASSWORD_SALT_ROUNDS))

    @staticmethod
    def verify_password(password: str, password_hash: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash)

    @staticmethod
    def generate_otp(length: int = 6) -> str:
        return "".join(secrets.choice(string.digits) for _ in range(length))

    @staticmethod
    def otp_expiry() -> datetime:
        return datetime.now() + timedelta(seconds=OTP_EXPIRY_SECONDS)

    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not any(c.islower() for c in password):
            return False, "Password must include lowercase letters."
        if not any(c.isupper() for c in password):
            return False, "Password must include uppercase letters."
        if not any(c.isdigit() for c in password):
            return False, "Password must include digits."
        if not any(c in string.punctuation for c in password):
            return False, "Password must include special characters."
        return True, "Strong password."
