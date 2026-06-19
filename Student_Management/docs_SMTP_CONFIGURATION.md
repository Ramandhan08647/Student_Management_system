# SMTP Configuration Guide

ASMRS uses SMTP to send email notifications and OTP verification codes. Follow these steps to configure SMTP successfully.

## Step 1: Copy the example file
Create a `.env` file in the project root by copying `.env.example`.

## Step 2: Add your SMTP settings
Update the `.env` file with your provider details:

- `SMTP_SERVER`: your email provider SMTP host
- `SMTP_PORT`: port number (usually 587 for TLS or 465 for SSL)
- `SMTP_USER`: the email address you send from
- `SMTP_PASSWORD`: the account password or app password
- `SMTP_USE_TLS`: `True` for TLS
- `SMTP_USE_SSL`: `True` for SSL (use either TLS or SSL, not both)
- `SMTP_FROM_NAME`: display sender name
- `SMTP_FROM_ADDRESS`: sender email address

## Recommended Providers
- Gmail: `smtp.gmail.com`, port `587` with `SMTP_USE_TLS=True`
- Outlook: `smtp.office365.com`, port `587` with `SMTP_USE_TLS=True`
- Yahoo: `smtp.mail.yahoo.com`, port `587` with `SMTP_USE_TLS=True`

## Step 3: Enable application access
For Gmail and similar providers, use an app password if two-factor authentication is enabled. Do not use your normal account password unless your provider allows less secure apps.

## Step 4: Test email delivery
Run this command from the project root:

```bash
python -c "from send_smtp import send_smtp_email; print(send_smtp_email('recipient@example.com', 'SMTP Test', 'This is a test email.'))"
```

A successful send returns `True`.

## Step 5: Use SMTP in ASMRS
The application automatically reads SMTP settings from the `.env` file and `config.py`.

## Troubleshooting
- `SMTPAuthenticationError`: verify your username/password or app password.
- `gaierror`: check the SMTP host name and internet connection.
- `ConnectionRefusedError`: verify port and TLS/SSL settings.
