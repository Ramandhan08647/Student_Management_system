import tkinter as tk
from tkinter import ttk

from ui_style import BACKGROUND, SURFACE, TEXT, MUTED, FONT_TITLE, FONT_BASE

class ReportPage(tk.Frame):
    def __init__(self, parent, report_manager, *args, **kwargs):
        super().__init__(parent, bg=BACKGROUND, *args, **kwargs)
        self.report_manager = report_manager
        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="Reports", font=FONT_TITLE, fg=TEXT, bg=BACKGROUND)
        title.pack(anchor="nw", padx=24, pady=(16, 12))

        button_frame = tk.Frame(self, bg=BACKGROUND)
        button_frame.pack(fill="x", padx=24, pady=(0, 16))

        ttk.Button(button_frame, text="Generate Student Report", command=self._generate_student_report, style="Accent.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Generate Financial Report", command=self._generate_financial_report, style="Secondary.TButton").pack(side="left")

        self.output = tk.Text(self, height=18, bg=SURFACE, fg=TEXT, bd=1, relief="solid", font=FONT_BASE)
        self.output.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def _generate_student_report(self):
        report = self.report_manager.generate_student_report("STD-2026-0001")
        self._render_report(report)

    def _generate_financial_report(self):
        report = self.report_manager.generate_financial_report()
        self._render_report(report)

    def _render_report(self, report_data):
        self.output.delete("1.0", tk.END)
        for key, value in report_data.items():
            self.output.insert(tk.END, f"{key}: {value}\n")
