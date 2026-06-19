# Advanced Student Management Record System (ASMRS)

## Overview
Advanced Student Management Record System is a Python Tkinter application designed to manage admissions, student records, attendance, academics, fees, reports, and administrative functions for schools and training institutions.

## Features
- Professional splash screen and modern UI styling
- Secure authentication with registration and OTP verification
- Role-based access control for Administrator, Teacher, and Student
- Modular MVC design for scalability
- SQLite backend with support for future migration
- Audit logging and configuration storage

## Setup
1. Install Python 3.10+.
2. Open a terminal in the project directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Project Structure
- `main.py`: Application entrypoint and splash flow
- `config.py`: App settings and constants
- `database/`: Schema and database helper
- `authentication/`: Login, registration, OTP, and user management
- `dashboard/`: Dashboard UI
- `students/`: Student management module
- `teachers/`: Teacher management module
- `settings/`: Application settings manager

## Notes
- Email verification requires valid SMTP configuration in `config.py`.
- The app uses SQLite stored at `database/asmrs.db`.

## Future Expansion
- Add course, subject, attendance, results, fees, reports, notifications, and backup modules.
- Add dark mode, PDF export, and advanced analytics.
