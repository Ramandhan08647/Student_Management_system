import tkinter as tk
from tkinter import ttk

PRIMARY = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"
SECONDARY = "#0EA5E9"
SECONDARY_HOVER = "#0284C7"
BACKGROUND = "#548765"
SURFACE = "#FFFFFF"
BORDER = "#E5E7EB"
TEXT = "#111827"
MUTED = "#4B5563"
DANGER = "#DC2626"
FONT_BASE = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUBTITLE = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 10, "bold")


def apply_theme(root: tk.Tk):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=BACKGROUND)
    style.configure("Body.TFrame", background=BACKGROUND)
    style.configure("Card.TFrame", background=SURFACE, relief="flat")
    style.configure("Accent.TButton", background=PRIMARY, foreground="#FFFFFF", font=FONT_BUTTON, borderwidth=0, focusthickness=3, focuscolor="")
    style.map("Accent.TButton", background=[("active", PRIMARY_HOVER)])
    style.configure("Secondary.TButton", background=SECONDARY, foreground="#FFFFFF", font=FONT_BUTTON, borderwidth=0)
    style.map("Secondary.TButton", background=[("active", SECONDARY_HOVER)])
    style.configure("Flat.TButton", background=BACKGROUND, foreground=PRIMARY, font=FONT_BUTTON, borderwidth=0)
    style.configure("Card.TEntry", fieldbackground=SURFACE, background=SURFACE, foreground=TEXT, bordercolor=BORDER, borderwidth=1, padding=8)
    style.configure("Card.TCombobox", fieldbackground=SURFACE, background=SURFACE, foreground=TEXT, bordercolor=BORDER, padding=8)
    style.configure("Card.Treeview", background=SURFACE, fieldbackground=SURFACE, foreground=TEXT)
    style.configure("Treeview.Heading", background=BACKGROUND, foreground=TEXT, font=FONT_BASE)
    style.configure("Header.TLabel", background=BACKGROUND, foreground=TEXT, font=("Segoe UI", 26, "bold"))
    style.configure("Subtitle.TLabel", background=BACKGROUND, foreground=MUTED, font=FONT_SUBTITLE)
    style.configure("Section.TLabel", background=SURFACE, foreground=TEXT, font=("Segoe UI", 12, "bold"))
    style.configure("Small.TLabel", background=BACKGROUND, foreground=MUTED, font=FONT_BASE)
    style.configure("Danger.TLabel", background=BACKGROUND, foreground=DANGER, font=FONT_BASE)
    style.configure("Accent.TLabel", background=BACKGROUND, foreground=PRIMARY, font=FONT_BASE)
    root.configure(bg=BACKGROUND)
