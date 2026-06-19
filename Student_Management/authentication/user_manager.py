from datetime import datetime
from typing import Optional
import re

from database.database import Database
from authentication.auth_utils import AuthUtils
from config import ROLE_ADMIN, ROLE_TEACHER, ROLE_STUDENT

class UserManager:
    def __init__(self, db: Database):
        self.db = db

    def register_user(self, full_name: str, username: str, email: str, phone: str, gender: str, dob: str, role: str, password: str) -> dict:
        if not username or not email or not password:
            raise ValueError("Username, email, and password are required.")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")

        if self.user_exists(username=username):
            raise ValueError("Username already exists.")

        if self.user_exists(email=email):
            raise ValueError("Email address already registered.")

        valid_password, message = AuthUtils.validate_password_strength(password)
        if not valid_password:
            raise ValueError(message)

        password_hash = AuthUtils.hash_password(password)
        now = self.db.current_timestamp()

        user_id = self.db.insert(
            "INSERT INTO users (full_name, username, email, phone, gender, dob, role, password_hash, is_active, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (full_name, username, email, phone, gender, dob, role, password_hash, 0, now, now),
        )

        return {"id": user_id, "username": username, "email": email, "role": role}

    def user_exists(self, username: str = None, email: str = None) -> bool:
        if username:
            result = self.db.fetchone("SELECT id FROM users WHERE username = ?", (username,))
            if result:
                return True
        if email:
            result = self.db.fetchone("SELECT id FROM users WHERE email = ?", (email,))
            if result:
                return True
        return False

    def login_user(self, username: str, password: str) -> Optional[dict]:
        user = self.db.fetchone("SELECT * FROM users WHERE username = ?", (username,))
        if not user:
            return None

        if not user["is_active"]:
            return None

        if AuthUtils.verify_password(password, user["password_hash"]):
            return {
                "id": user["id"],
                "username": user["username"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user["role"],
            }
        return None

    def activate_user(self, email: str):
        now = self.db.current_timestamp()
        self.db.execute(
            "UPDATE users SET is_active = 1, updated_at = ? WHERE email = ?",
            (now, email),
        )

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.db.fetchone("SELECT * FROM users WHERE email = ?", (email,))
        return dict(user) if user else None

    def log_action(self, user_id: int, action: str, entity: str = None, entity_id: str = None, details: str = None):
        timestamp = self.db.current_timestamp()
        self.db.insert(
            "INSERT INTO audit_logs (user_id, action, entity, entity_id, details, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, action, entity, entity_id, details, timestamp),
        )
