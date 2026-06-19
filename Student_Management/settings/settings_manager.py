import json
from pathlib import Path
from typing import Any, Optional

from config import CONFIG_PATH, DEFAULT_SETTINGS

class SettingsManager:
    def __init__(self):
        self.config_path = CONFIG_PATH
        self.settings = self._load_settings()

    def _load_settings(self) -> dict:
        if not self.config_path.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_settings(DEFAULT_SETTINGS)
        with open(self.config_path, "r", encoding="utf-8") as config_file:
            return json.load(config_file)

    def _save_settings(self, settings: dict) -> None:
        with open(self.config_path, "w", encoding="utf-8") as config_file:
            json.dump(settings, config_file, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
        self._save_settings(self.settings)
