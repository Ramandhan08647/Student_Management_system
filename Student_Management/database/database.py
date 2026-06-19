import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json

from config import DATABASE_PATH, CONFIG_PATH, DEFAULT_SETTINGS

class Database:
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self.connection = None
        self._ensure_database()

    def _ensure_database(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.connection.row_factory = sqlite3.Row
        self._initialize_schema()
        self._initialize_settings()

    def _initialize_schema(self):
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            self.connection.executescript(schema_file.read())
        self.connection.commit()

    def _initialize_settings(self):
        if not CONFIG_PATH.exists():
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_PATH, "w", encoding="utf-8") as config_file:
                json.dump(DEFAULT_SETTINGS, config_file, indent=4)

    def execute(self, query: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        return cursor

    def fetchone(self, query: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetchall(self, query: str, params: Optional[tuple] = None) -> list[sqlite3.Row]:
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def insert(self, query: str, params: tuple) -> int:
        cursor = self.execute(query, params)
        return cursor.lastrowid

    def close(self):
        if self.connection:
            self.connection.close()

    def get_setting(self, key: str) -> Any:
        cursor = self.fetchone("SELECT value FROM settings WHERE key = ?", (key,))
        return cursor["value"] if cursor else None

    def set_setting(self, key: str, value: Any):
        if self.get_setting(key) is None:
            self.insert("INSERT INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
        else:
            self.execute("UPDATE settings SET value = ? WHERE key = ?", (str(value), key))

    def current_timestamp(self) -> str:
        return datetime.now().isoformat(sep=" ", timespec="seconds")
