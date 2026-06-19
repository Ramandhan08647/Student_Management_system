import tkinter as tk
from tkinter import ttk

from ui_style import BACKGROUND, SURFACE, BORDER, TEXT, MUTED, FONT_BASE, FONT_TITLE

class DashboardLayout(tk.Frame):
    def __init__(self, parent, session: dict = None):
        super().__init__(parent, bg=BACKGROUND)
        self.session = session or {}
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=BACKGROUND)
        header.pack(fill="x", padx=24, pady=(20, 12))

        tk.Label(header, text=f"Welcome back, {self.session.get('full_name', 'User')}", font=FONT_TITLE, bg=BACKGROUND, fg=TEXT).pack(anchor="w")
        tk.Label(header, text="Your student management workspace, simplified.", font=FONT_BASE, bg=BACKGROUND, fg=MUTED).pack(anchor="w", pady=(4, 0))

        top_frame = tk.Frame(self, bg=BACKGROUND)
        top_frame.pack(fill="both", expand=True, padx=24, pady=16)

        stats_card = tk.Frame(top_frame, bg=SURFACE, bd=0, relief="flat", highlightthickness=1, highlightbackground=BORDER)
        stats_card.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=0)
        tk.Label(stats_card, text="Quick Stats", font=("Segoe UI", 16, "bold"), bg=SURFACE, fg=TEXT).pack(anchor="w", padx=20, pady=(20, 12))

        stats_items = [
            ("Students", "128"),
            ("Teachers", "18"),
            ("Courses", "24"),
            ("Attendance", "96%"),
        ]
        for label, value in stats_items:
            row = tk.Frame(stats_card, bg=SURFACE)
            row.pack(fill="x", padx=20, pady=8)
            tk.Label(row, text=label, font=FONT_BASE, bg=SURFACE, fg=MUTED).pack(side="left")
            tk.Label(row, text=value, font=("Segoe UI", 12, "bold"), bg=SURFACE, fg=TEXT).pack(side="right")

        navigation_card = tk.Frame(top_frame, bg=SURFACE, bd=0, relief="flat", highlightthickness=1, highlightbackground=BORDER)
        navigation_card.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=0)
        tk.Label(navigation_card, text="Quick Actions", font=("Segoe UI", 16, "bold"), bg=SURFACE, fg=TEXT).pack(anchor="w", padx=20, pady=(20, 12))

        for label in ["Students", "Teachers", "Results", "Reports", "Notifications"]:
            action_button = ttk.Button(navigation_card, text=label, style="Flat.TButton")
            action_button.pack(fill="x", padx=20, pady=8)
