import tkinter as tk
from tkinter import ttk
from pathlib import Path
from threading import Thread
import time

from config import APP_NAME, APP_VERSION, SCHOOL_NAME, SCHOOL_LOGO
from authentication.auth_window import AuthWindow
from dashboard.dashboard_window import DashboardWindow
from database.database import Database
from ui_style import apply_theme, BACKGROUND, PRIMARY, SURFACE, TEXT, MUTED, FONT_BASE, FONT_TITLE, FONT_SUBTITLE

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Loading...")
        self.geometry("600x360")
        self.configure(bg=PRIMARY)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.overrideredirect(True)

        self.logo = tk.PhotoImage(file=str(SCHOOL_LOGO)) if Path(SCHOOL_LOGO).exists() else None
        self._build_ui()

    def _build_ui(self):
        container = tk.Frame(self, bg=PRIMARY)
        container.place(relx=0.5, rely=0.5, anchor="center")

        if self.logo:
            logo_label = tk.Label(container, image=self.logo, bg=PRIMARY)
            logo_label.pack(pady=(0, 10))

        title = tk.Label(container, text=SCHOOL_NAME, font=FONT_TITLE, fg=SURFACE, bg=PRIMARY)
        title.pack()

        subtitle = tk.Label(container, text=APP_NAME, font=FONT_SUBTITLE, fg=MUTED, bg=PRIMARY)
        subtitle.pack(pady=(4, 20))

        self.progress = ttk.Progressbar(container, orient="horizontal", length=420, mode="determinate")
        self.progress.pack(pady=(0, 16))

        version = tk.Label(container, text=f"Version {APP_VERSION}", font=FONT_BASE, fg=MUTED, bg=PRIMARY)
        version.pack()

    def start(self):
        self.progress_value = 0
        self.after(50, self._step)

    def _step(self):
        self.progress_value += 2
        self.progress['value'] = self.progress_value
        if self.progress_value < 100:
            self.after(80, self._step)
        else:
            self.destroy()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        apply_theme(self)
        self.withdraw()
        self.title(APP_NAME)
        self.geometry("1200x780")
        self.configure(bg=BACKGROUND)
        self.minsize(1100, 720)
        self.db = Database()
        self.session = {}
        self._show_splash()

    def _show_splash(self):
        splash = SplashScreen(self)
        splash.start()
        self.after(4200, self._start_auth)

    def _start_auth(self):
        self.deiconify()
        self.auth_window = AuthWindow(self, self.db, self._open_dashboard)
        self.auth_window.pack(fill="both", expand=True)

    def _open_dashboard(self, user: dict):
        self.auth_window.destroy()
        self.session = user
        self.dashboard_window = DashboardWindow(self, session=user)
        self.dashboard_window.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
