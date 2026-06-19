import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

from authentication.user_manager import UserManager
from authentication.auth_utils import AuthUtils
from authentication.email_service import EmailService
from database.database import Database
from config import ROLE_ADMIN, ROLE_TEACHER, ROLE_STUDENT
from ui_style import BACKGROUND, SURFACE, BORDER, TEXT, MUTED, FONT_BASE, FONT_TITLE, FONT_SUBTITLE

class AuthWindow(tk.Frame):
    def __init__(self, parent, db: Database, login_success_callback=None):
        super().__init__(parent, bg=BACKGROUND)
        self.db = db
        self.login_success_callback = login_success_callback
        self.user_manager = UserManager(db)
        self.email_service = EmailService()
        self.otp_code = None
        self.otp_expiry = None
        self._build_ui()

    def _build_ui(self):
        container = tk.Frame(self, bg=BACKGROUND)
        container.pack(fill="both", expand=True, padx=40, pady=24)

        header = tk.Label(container, text="Secure Login Portal", font=FONT_TITLE, fg=TEXT, bg=BACKGROUND)
        header.pack(pady=(16, 12))

        subheader = tk.Label(container, text="Access your ASMRS workspace with your account.", font=FONT_SUBTITLE, fg=MUTED, bg=BACKGROUND)
        subheader.pack(pady=(0, 20))

        card = tk.Frame(container, bg=SURFACE, bd=0, relief="flat", highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="both", expand=True, padx=12, pady=8)

        self._build_login_form(card)

    def _build_login_form(self, parent):
        form_frame = tk.Frame(parent, bg=SURFACE)
        form_frame.pack(padx=28, pady=28, fill="x")

        username_label = tk.Label(form_frame, text="Username", font=FONT_BASE, fg=TEXT, bg=SURFACE)
        username_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.username_var, style="Card.TEntry")
        username_entry.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        password_label = tk.Label(form_frame, text="Password", font=FONT_BASE, fg=TEXT, bg=SURFACE)
        password_label.grid(row=2, column=0, sticky="w", pady=(0, 6))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(form_frame, textvariable=self.password_var, style="Card.TEntry", show="*")
        self.password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 12))

        show_password_check = tk.Checkbutton(form_frame, text="Show Password", variable=tk.IntVar(), command=self._toggle_password, bg=SURFACE, fg=TEXT, font=FONT_BASE, activebackground=SURFACE, activeforeground=TEXT, bd=0, highlightthickness=0)
        show_password_check.grid(row=4, column=0, sticky="w", pady=(0, 12))

        remember_check = tk.Checkbutton(form_frame, text="Remember Me", bg=SURFACE, fg=TEXT, font=FONT_BASE, activebackground=SURFACE, activeforeground=TEXT, bd=0, highlightthickness=0)
        remember_check.grid(row=5, column=0, sticky="w", pady=(0, 24))

        login_button = ttk.Button(form_frame, text="Login", command=self._login, style="Accent.TButton")
        login_button.grid(row=6, column=0, sticky="ew", pady=(0, 10))

        forgot_button = ttk.Button(form_frame, text="Forgot Password", command=self._forgot_password, style="Flat.TButton")
        forgot_button.grid(row=7, column=0, sticky="ew", pady=(0, 8))

        register_button = ttk.Button(form_frame, text="Register", command=self._show_registration, style="Secondary.TButton")
        register_button.grid(row=8, column=0, sticky="ew", pady=(0, 4))

        form_frame.columnconfigure(0, weight=1)

    def _toggle_password(self):
        if self.password_entry.cget("show") == "":
            self.password_entry.config(show="*")
        else:
            self.password_entry.config(show="")

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Login Error", "Please enter both username and password.")
            return

        user = self.user_manager.login_user(username, password)
        if not user:
            messagebox.showerror("Login Failed", "Invalid credentials or account inactive.")
            return

        messagebox.showinfo("Welcome", f"Welcome back, {user['full_name']}.")
        if self.login_success_callback:
            self.login_success_callback(user)

    def _forgot_password(self):
        messagebox.showinfo("Forgot Password", "Please contact the administrator to reset your password.")

    def _show_registration(self):
        RegistrationWindow(self.master, self.db)

class RegistrationWindow(tk.Toplevel):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.title("Create Account - ASMRS")
        self.geometry("750x850")
        self.configure(bg="#F3F4F6")
        self.resizable(False, False)
        self.db = db
        self.user_manager = UserManager(db)
        self.email_service = EmailService()
        self.otp_code = None
        self.otp_expiry = None
        self._build_ui()

    def _build_ui(self):
        main_container = tk.Frame(self, bg="#F3F4F6")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        header_section = tk.Frame(main_container, bg="#F3F4F6")
        header_section.pack(fill="x", pady=(0, 24))

        title = tk.Label(header_section, text="Create Your Account", font=("Poppins", 24, "bold"), fg="#111827", bg="#F3F4F6")
        title.pack(anchor="w")

        subtitle = tk.Label(header_section, text="Register to access ASMRS and manage your educational records", font=("Segoe UI", 11), fg="#6B7280", bg="#F3F4F6")
        subtitle.pack(anchor="w", pady=(6, 0))

        card_frame = tk.Frame(main_container, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E5E7EB")
        card_frame.pack(fill="both", expand=True)

        inner_form = tk.Frame(card_frame, bg="#FFFFFF")
        inner_form.pack(fill="both", expand=True, padx=28, pady=28)

        section_row = 0

        personal_title = tk.Label(inner_form, text="Personal Information", font=("Poppins", 12, "bold"), fg="#111827", bg="#FFFFFF")
        personal_title.grid(row=section_row, column=0, columnspan=2, sticky="w", pady=(0, 16))
        section_row += 1

        self.fields = {}

        tk.Label(inner_form, text="Full Name *", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=0, sticky="w", pady=(0, 6))
        self.fields["full_name"] = tk.StringVar()
        tk.Entry(inner_form, textvariable=self.fields["full_name"], font=("Segoe UI", 10), bd=1, relief="solid").grid(row=section_row + 1, column=0, sticky="ew", pady=(0, 12))

        tk.Label(inner_form, text="Gender", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=1, sticky="w", pady=(0, 6), padx=(12, 0))
        self.fields["gender"] = tk.StringVar(value="Prefer not to say")
        ttk.Combobox(inner_form, textvariable=self.fields["gender"], state="readonly", values=["Male", "Female", "Prefer not to say"], font=("Segoe UI", 10)).grid(row=section_row + 1, column=1, sticky="ew", pady=(0, 12), padx=(12, 0))

        section_row += 2

        tk.Label(inner_form, text="Date of Birth", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=0, sticky="w", pady=(0, 6))
        self.fields["dob"] = tk.StringVar()
        tk.Entry(inner_form, textvariable=self.fields["dob"], font=("Segoe UI", 10), bd=1, relief="solid").grid(row=section_row + 1, column=0, sticky="ew", pady=(0, 12))

        tk.Label(inner_form, text="Phone Number", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=1, sticky="w", pady=(0, 6), padx=(12, 0))
        self.fields["phone"] = tk.StringVar()
        tk.Entry(inner_form, textvariable=self.fields["phone"], font=("Segoe UI", 10), bd=1, relief="solid").grid(row=section_row + 1, column=1, sticky="ew", pady=(0, 12), padx=(12, 0))

        section_row += 2

        separator1 = tk.Frame(inner_form, bg="#E5E7EB", height=1)
        separator1.grid(row=section_row, column=0, columnspan=2, sticky="ew", pady=12)
        section_row += 1

        account_title = tk.Label(inner_form, text="Account Information", font=("Poppins", 12, "bold"), fg="#111827", bg="#FFFFFF")
        account_title.grid(row=section_row, column=0, columnspan=2, sticky="w", pady=(0, 16))
        section_row += 1

        tk.Label(inner_form, text="Username *", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=0, sticky="w", pady=(0, 6))
        self.fields["username"] = tk.StringVar()
        tk.Entry(inner_form, textvariable=self.fields["username"], font=("Segoe UI", 10), bd=1, relief="solid").grid(row=section_row + 1, column=0, sticky="ew", pady=(0, 12))

        tk.Label(inner_form, text="Role", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=1, sticky="w", pady=(0, 6), padx=(12, 0))
        self.fields["role"] = tk.StringVar(value=ROLE_STUDENT)
        ttk.Combobox(inner_form, textvariable=self.fields["role"], state="readonly", values=[ROLE_ADMIN, ROLE_TEACHER, ROLE_STUDENT], font=("Segoe UI", 10)).grid(row=section_row + 1, column=1, sticky="ew", pady=(0, 12), padx=(12, 0))

        section_row += 2

        tk.Label(inner_form, text="Email Address *", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=0, columnspan=2, sticky="w", pady=(0, 6))
        self.fields["email"] = tk.StringVar()
        tk.Entry(inner_form, textvariable=self.fields["email"], font=("Segoe UI", 10), bd=1, relief="solid").grid(row=section_row + 1, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        section_row += 2

        separator2 = tk.Frame(inner_form, bg="#E5E7EB", height=1)
        separator2.grid(row=section_row, column=0, columnspan=2, sticky="ew", pady=12)
        section_row += 1

        security_title = tk.Label(inner_form, text="Security", font=("Poppins", 12, "bold"), fg="#111827", bg="#FFFFFF")
        security_title.grid(row=section_row, column=0, columnspan=2, sticky="w", pady=(0, 16))
        section_row += 1

        tk.Label(inner_form, text="Password *", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=0, sticky="w", pady=(0, 6))
        self.fields["password"] = tk.StringVar()
        tk.Entry(inner_form, textvariable=self.fields["password"], font=("Segoe UI", 10), bd=1, relief="solid", show="*").grid(row=section_row + 1, column=0, sticky="ew", pady=(0, 12))

        tk.Label(inner_form, text="Confirm Password *", font=("Segoe UI", 10), fg="#374151", bg="#FFFFFF").grid(row=section_row, column=1, sticky="w", pady=(0, 6), padx=(12, 0))
        self.fields["confirm_password"] = tk.StringVar()
        tk.Entry(inner_form, textvariable=self.fields["confirm_password"], font=("Segoe UI", 10), bd=1, relief="solid", show="*").grid(row=section_row + 1, column=1, sticky="ew", pady=(0, 12), padx=(12, 0))

        section_row += 2

        tk.Label(inner_form, text="• At least 8 characters\n• Mix of upper and lower case letters\n• At least one number\n• At least one special character (!@#$%^&*)", font=("Segoe UI", 9), fg="#6B7280", bg="#FFFFFF").grid(row=section_row, column=0, columnspan=2, sticky="w", pady=(0, 20))

        section_row += 1

        self.message_label = tk.Label(inner_form, text="", fg="#DC2626", bg="#FFFFFF", font=("Segoe UI", 10), wraplength=400)
        self.message_label.grid(row=section_row, column=0, columnspan=2, sticky="w", pady=(0, 16))

        section_row += 1

        register_button = tk.Button(inner_form, text="Create Account", command=self._register_user, bg="#1E3A8A", fg="#FFFFFF", font=("Segoe UI", 11, "bold"), bd=0, padx=16, pady=12, cursor="hand2", activebackground="#1E40AF")
        register_button.grid(row=section_row, column=0, columnspan=2, sticky="ew")

        cancel_button = tk.Button(inner_form, text="Cancel", command=self.destroy, bg="#E5E7EB", fg="#374151", font=("Segoe UI", 10), bd=0, padx=16, pady=10, cursor="hand2", activebackground="#D1D5DB")
        cancel_button.grid(row=section_row + 1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        inner_form.columnconfigure(0, weight=1)
        inner_form.columnconfigure(1, weight=1)

    def _register_user(self):
        data = {k: v.get().strip() for k, v in self.fields.items()}
        if not data["full_name"] or not data["username"] or not data["email"] or not data["password"] or not data["confirm_password"]:
            self.message_label.config(text="Please complete all required fields.")
            return
        if data["password"] != data["confirm_password"]:
            self.message_label.config(text="Passwords do not match.")
            return

        try:
            self.user_manager.register_user(
                data["full_name"],
                data["username"],
                data["email"],
                data["phone"],
                data["gender"],
                data["dob"],
                data["role"],
                data["password"],
            )
            self._send_otp(data["email"], data["full_name"])
        except ValueError as error:
            self.message_label.config(text=str(error))

    def _send_otp(self, email: str, username: str = None):
        self.otp_code = AuthUtils.generate_otp()
        self.otp_expiry = AuthUtils.otp_expiry()
        recipient_name = username or email.split("@")[0]
        if self.email_service.send_verification_email(email, recipient_name, self.otp_code):
            self._show_otp_dialog(email)
        else:
            messagebox.showerror("Verification Error", "Unable to send verification email. Please check your SMTP settings.")

    def _show_otp_dialog(self, email: str):
        otp_window = tk.Toplevel(self)
        otp_window.title("Verify Email")
        otp_window.geometry("420x260")
        otp_window.configure(bg="#F8FAFC")
        otp_window.resizable(False, False)

        tk.Label(otp_window, text="Enter the OTP sent to your email", font=("Poppins", 14, "bold"), fg="#111827", bg="#F8FAFC").pack(pady=(24, 8))
        tk.Label(otp_window, text="Check your inbox and paste the code below.", font=("Segoe UI", 10), fg="#6B7280", bg="#F8FAFC").pack(pady=(0, 18))

        otp_var = tk.StringVar()
        otp_entry = tk.Entry(otp_window, textvariable=otp_var, font=("Segoe UI", 12), bd=1, relief="solid")
        otp_entry.pack(ipadx=64, ipady=8, pady=(0, 12))

        def verify():
            if not otp_var.get().strip():
                return
            if self.otp_code is None or self.otp_expiry is None or self.otp_expiry < datetime.now():
                messagebox.showerror("OTP Error", "The OTP code has expired.")
                return
            if otp_var.get().strip() != self.otp_code:
                messagebox.showerror("OTP Error", "Incorrect OTP code.")
                return
            self.user_manager.activate_user(email)
            messagebox.showinfo("Account Verified", "Your account has been activated successfully.")
            otp_window.destroy()
            self.destroy()

        verify_button = tk.Button(otp_window, text="Verify OTP", command=verify, bg="#10B981", fg="#FFFFFF", font=("Segoe UI", 11, "bold"), bd=0)
        verify_button.pack(pady=(14, 0))
