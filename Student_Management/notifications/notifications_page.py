import tkinter as tk
from tkinter import ttk

from ui_style import BACKGROUND, SURFACE, TEXT, MUTED, FONT_TITLE, FONT_BASE

class NotificationsPage(tk.Frame):
    def __init__(self, parent, notification_manager, *args, **kwargs):
        super().__init__(parent, bg=BACKGROUND, *args, **kwargs)
        self.notification_manager = notification_manager
        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="Notifications", font=FONT_TITLE, fg=TEXT, bg=BACKGROUND)
        title.pack(anchor="nw", padx=24, pady=(16, 12))

        action_frame = tk.Frame(self, bg=BACKGROUND)
        action_frame.pack(fill="x", padx=24, pady=(0, 16))

        ttk.Button(action_frame, text="Send Notification", command=self._send_notification, style="Accent.TButton").pack(side="left")

        self.notification_list = ttk.Treeview(self, columns=("title", "message", "sent_at"), show="headings", height=10, style="Card.Treeview")
        self.notification_list.heading("title", text="Title")
        self.notification_list.heading("message", text="Message")
        self.notification_list.heading("sent_at", text="Sent At")
        self.notification_list.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        self._load_notifications()

    def _load_notifications(self):
        items = self.notification_manager.list_notifications("Administrator")
        for item in items:
            self.notification_list.insert("", "end", values=(item["title"], item["message"], item["sent_at"]))

    def _send_notification(self):
        notification = self.notification_manager.send_notification(
            "System Announcement",
            "A new system update is available.",
            recipient_role="Administrator",
        )
        self.notification_list.insert("", "end", values=(notification["title"], notification["message"], notification["sent_at"]))
