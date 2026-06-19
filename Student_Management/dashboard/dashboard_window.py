import tkinter as tk
from tkinter import ttk

from ui_style import BACKGROUND, SURFACE, BORDER, TEXT, MUTED, FONT_TITLE, FONT_SUBTITLE

class DashboardWindow(tk.Frame):
    def __init__(self, parent, session: dict = None):
        super().__init__(parent, bg=BACKGROUND)
        self.session = session or {}
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=BACKGROUND)
        header.pack(fill="x", padx=24, pady=(16, 8))

        title = tk.Label(header, text="Dashboard", font=FONT_TITLE, bg=BACKGROUND, fg=TEXT)
        title.pack(side="left")

        summary_frame = tk.Frame(self, bg=BACKGROUND)
        summary_frame.pack(fill="both", expand=True, padx=24, pady=12)

        cards = [
            ("Total Students", "128"),
            ("Total Teachers", "18"),
            ("Total Courses", "24"),
            ("Attendance Today", "96%"),
        ]

        for idx, (label, value) in enumerate(cards):
            card = tk.Frame(summary_frame, bg=SURFACE, bd=0, relief="flat", highlightthickness=1, highlightbackground=BORDER)
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            tk.Label(card, text=label, font=FONT_BASE, fg=MUTED, bg=SURFACE).pack(anchor="w", padx=16, pady=(16, 4))
            tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), fg=TEXT, bg=SURFACE).pack(anchor="w", padx=16, pady=(0, 16))

        for column_index in range(4):
            summary_frame.grid_columnconfigure(column_index, weight=1)
