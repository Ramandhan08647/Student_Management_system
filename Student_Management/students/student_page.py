import tkinter as tk
from tkinter import ttk

from ui_style import BACKGROUND, SURFACE, BORDER, TEXT, MUTED, FONT_TITLE, FONT_BASE

class StudentsPage(tk.Frame):
    def __init__(self, parent, manager, *args, **kwargs):
        super().__init__(parent, bg=BACKGROUND, *args, **kwargs)
        self.manager = manager
        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="Student Management", font=FONT_TITLE, bg=BACKGROUND, fg=TEXT)
        title.pack(anchor="nw", padx=24, pady=(16, 10))

        search_frame = tk.Frame(self, bg=BACKGROUND)
        search_frame.pack(fill="x", padx=24, pady=(0, 16))

        tk.Label(search_frame, text="Search students", font=FONT_BASE, fg=MUTED, bg=BACKGROUND).pack(side="left", padx=(0, 8))
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, style="Card.TEntry").pack(side="left", fill="x", expand=True, padx=(0, 12))
        ttk.Button(search_frame, text="Search", command=self._search_students, style="Accent.TButton").pack(side="left")

        self.tree = ttk.Treeview(self, columns=("student_id", "name", "gender", "class", "department"), show="headings", selectmode="browse", style="Card.Treeview")
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("class", text="Class")
        self.tree.heading("department", text="Department")
        self.tree.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def _search_students(self):
        search_term = self.search_var.get().strip()
        results = self.manager.search_students(search_term)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for student in results:
            self.tree.insert("", "end", values=(
                student.get("student_id"),
                f"{student.get('first_name')} {student.get('last_name')}",
                student.get("gender"),
                student.get("class"),
                student.get("department"),
            ))
