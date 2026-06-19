import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "asmrs.db"
CONFIG_PATH = BASE_DIR / "database" / "config.json"
LOGS_PATH = BASE_DIR / "logs"
ASSETS_PATH = BASE_DIR / "assets"
BACKUP_PATH = BASE_DIR / "backups"

APP_VERSION = "1.0.0"
APP_NAME = "Student Management Record System"
SCHOOL_NAME = "Limkokwing University"
SCHOOL_LOGO = ASSETS_PATH / "school_logo.png"

ROLE_ADMIN = "Administrator"
ROLE_TEACHER = "Teacher"
ROLE_STUDENT = "Student"

PASSWORD_SALT_ROUNDS = 12
OTP_EXPIRY_SECONDS = 300

DEFAULT_THEME = "light"

EMAIL_SETTINGS = {
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "smtp_user": "noreply@example.com",
    "smtp_password": "Rema~drex@01",
    "use_tls": True,
}

DEFAULT_SETTINGS = {
    "school_name": SCHOOL_NAME,
    "school_logo": str(SCHOOL_LOGO),
    "theme": DEFAULT_THEME,
    "email_settings": EMAIL_SETTINGS,
    "otp_expiry_seconds": OTP_EXPIRY_SECONDS,
}
