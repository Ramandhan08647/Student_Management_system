import tkinter as tk
from tkinter import ttk

from ui_style import BACKGROUND, SURFACE, BORDER, TEXT, MUTED, FONT_TITLE, FONT_BASE

class TeachersPage(tk.Frame):
    def __init__(self, parent, manager, *args, **kwargs):
        super().__init__(parent, bg=BACKGROUND, *args, **kwargs)
        self.manager = manager
        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="Teacher Management", font=FONT_TITLE, bg=BACKGROUND, fg=TEXT)
        title.pack(anchor="nw", padx=24, pady=(16, 10))

        search_frame = tk.Frame(self, bg=BACKGROUND)
        search_frame.pack(fill="x", padx=24, pady=(0, 16))

        tk.Label(search_frame, text="Search teachers", font=FONT_BASE, fg=MUTED, bg=BACKGROUND).pack(side="left", padx=(0, 8))
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, style="Card.TEntry").pack(side="left", fill="x", expand=True, padx=(0, 12))
        ttk.Button(search_frame, text="Search", command=self._search_teachers, style="Accent.TButton").pack(side="left")

        self.tree = ttk.Treeview(self, columns=("teacher_id", "name", "qualification", "department", "subject"), show="headings", selectmode="browse", style="Card.Treeview")
        self.tree.heading("teacher_id", text="Teacher ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("qualification", text="Qualification")
        self.tree.heading("department", text="Department")
        self.tree.heading("subject", text="Subject")
        self.tree.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def _search_teachers(self):
        search_term = self.search_var.get().strip()
        results = self.manager.search_teachers(search_term)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for teacher in results:
            self.tree.insert("", "end", values=(
                teacher.get("teacher_id"),
                teacher.get("full_name"),
                teacher.get("qualification"),
                teacher.get("department"),
                teacher.get("subject"),
            ))
