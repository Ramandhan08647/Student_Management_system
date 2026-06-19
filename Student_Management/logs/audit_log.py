from datetime import datetime

class AuditLog:
    def __init__(self, db=None):
        self.db = db

    def record(self, user_id: int, action: str, entity: str = None, entity_id: str = None, details: str = None) -> dict:
        entry = {
            "user_id": user_id,
            "action": action,
            "entity": entity,
            "entity_id": entity_id,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        }
        return entry
