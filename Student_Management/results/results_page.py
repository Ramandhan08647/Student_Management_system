import tkinter as tk
from tkinter import ttk

from ui_style import BACKGROUND, SURFACE, TEXT, MUTED, FONT_TITLE, FONT_BASE

class ResultsPage(tk.Frame):
    def __init__(self, parent, result_manager, *args, **kwargs):
        super().__init__(parent, bg=BACKGROUND, *args, **kwargs)
        self.result_manager = result_manager
        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="Results", font=("Poppins", 18, "bold"), fg="#111827", bg="#F8FAFC")
        title.pack(anchor="nw", padx=24, pady=(16, 12))

        input_frame = tk.Frame(self, bg="#F8FAFC")
        input_frame.pack(fill="x", padx=24, pady=(0, 16))

        self.test_score = tk.StringVar()
        self.assignment_score = tk.StringVar()
        self.exam_score = tk.StringVar()

        tk.Label(input_frame, text="Test Score", font=("Segoe UI", 10), fg="#374151", bg="#F8FAFC").grid(row=0, column=0, sticky="w")
        tk.Entry(input_frame, textvariable=self.test_score, font=("Segoe UI", 10), bd=1, relief="solid").grid(row=1, column=0, padx=(0, 12), sticky="ew")

        tk.Label(input_frame, text="Assignment Score", font=("Segoe UI", 10), fg="#374151", bg="#F8FAFC").grid(row=0, column=1, sticky="w")
        tk.Entry(input_frame, textvariable=self.assignment_score, font=("Segoe UI", 10), bd=1, relief="solid").grid(row=1, column=1, padx=(0, 12), sticky="ew")

        tk.Label(input_frame, text="Exam Score", font=("Segoe UI", 10), fg="#374151", bg="#F8FAFC").grid(row=0, column=2, sticky="w")
        tk.Entry(input_frame, textvariable=self.exam_score, font=("Segoe UI", 10), bd=1, relief="solid").grid(row=1, column=2, sticky="ew")

        tk.Button(input_frame, text="Calculate Result", command=self._calculate_result, bg="#1E3A8A", fg="#FFFFFF", bd=0, padx=14, pady=10).grid(row=1, column=3, padx=(12, 0))

        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(2, weight=1)

        self.result_display = tk.Text(self, height=14, bg=SURFACE, fg=TEXT, bd=1, relief="solid", font=FONT_BASE)
        self.result_display.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def _calculate_result(self):
        try:
            result = self.result_manager.calculate_result(
                float(self.test_score.get()),
                float(self.assignment_score.get()),
                float(self.exam_score.get()),
            )
            self.result_display.delete("1.0", tk.END)
            for key, value in result.items():
                self.result_display.insert(tk.END, f"{key}: {value}\n")
        except ValueError:
            self.result_display.delete("1.0", tk.END)
            self.result_display.insert(tk.END, "Please enter valid numeric scores.")
