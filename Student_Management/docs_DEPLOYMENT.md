# Deployment Guide

## Packaging
- Use PyInstaller or similar tool to create a standalone executable.
- Include the `database`, `assets`, `authentication`, `dashboard`, `students`, `teachers`, and `settings` folders.

## Deployment Steps
1. Install project dependencies.
2. Configure SMTP settings in `config.py`.
3. Test the application locally.
4. Package the app and distribute the executable to end users.

## Notes
- Ensure `assets/school_logo.png` is included for the splash screen.
- Keep the SQLite database in the `database` folder for portability.
