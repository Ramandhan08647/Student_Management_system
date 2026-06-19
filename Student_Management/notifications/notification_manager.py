from datetime import datetime
from typing import List, Dict, Any

class NotificationManager:
    def __init__(self, db=None):
        self.db = db

    def send_notification(self, title: str, message: str, recipient_role: str = "Administrator") -> Dict[str, Any]:
        notification = {
            "title": title,
            "message": message,
            "recipient_role": recipient_role,
            "sent_at": datetime.now().isoformat(),
            "is_read": False,
        }
        return notification

    def list_notifications(self, recipient_role: str) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Test Notification",
                "message": "This is a sample notification.",
                "recipient_role": recipient_role,
                "sent_at": datetime.now().isoformat(),
                "is_read": False,
            }
        ]
