"""
email_blaster.py — Send emails via smtplib (no dependencies)
--------------------------------------------------------------
Setup:
  1. Use a Gmail account
  2. Enable App Passwords at: https://myaccount.google.com/apppasswords
  3. Fill in your Gmail + App Password below
  4. Run: python email_blaster.py
"""

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─────────────────────────────────────────────
#  CONFIG — fill these in
# ─────────────────────────────────────────────

GMAIL_ADDRESS  = "murdermaster.1234.mc@gmail.com"
GMAIL_APP_PASS = "aduk stcc ocve tyqm"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# ─────────────────────────────────────────────
#  SEND FUNCTION
# ─────────────────────────────────────────────

def send_email(smtp: smtplib.SMTP, to: str, subject: str, body: str) -> bool:
    try:
        msg = MIMEMultipart()
        msg["From"]    = GMAIL_ADDRESS
        msg["To"]      = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        smtp.sendmail(GMAIL_ADDRESS, to, msg.as_string())
        return True
    except Exception as e:
        print(f"      ⚠  Error: {e}")
        return False

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    print("\n╔══════════════════════════════╗")
    print("║      EMAIL BLASTER 📧         ║")
    print("╚══════════════════════════════╝\n")

    # — Inputs —
    to = input("  Recipient email: ").strip()
    if "@" not in to:
        print("  ❌ Invalid email address.")
        return

    subject = input("  Subject: ").strip()

    print("  Body (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    body = "\n".join(lines).strip()

    if not body:
        print("  ❌ Body cannot be empty.")
        return

    while True:
        try:
            count = int(input("  How many times to send: ").strip())
            if count < 1:
                raise ValueError
            break
        except ValueError:
            print("  ⚠  Enter a positive whole number.")

    # — Confirm —
    print(f"\n  📋 Summary")
    print(f"     To      : {to}")
    print(f"     Subject : {subject}")
    print(f"     Body    : {body[:60]}{'...' if len(body) > 60 else ''}")
    print(f"     Count   : {count}x")
    if input("\n  Send? (y/n): ").strip().lower() != "y":
        print("\n  Aborted.")
        return

    # — Connect —
    print("\n  Connecting to Gmail SMTP...")
    try:
        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASS)
        print("  ✅ Connected.\n")
    except Exception as e:
        print(f"  ❌ SMTP login failed: {e}")
        return

    # — Send —
    success = 0
    failed  = 0

    for i in range(1, count + 1):
        print(f"  Sending [{i}/{count}]...", end=" ", flush=True)
        ok = send_email(smtp, to, subject, body)
        if ok:
            print("✅")
            success += 1
        else:
            print("❌")
            failed += 1
        if i < count:
            time.sleep(0.5)

    smtp.quit()
    print(f"\n  ✔  Done — {success}/{count} sent, {failed} failed.\n")


if __name__ == "__main__":
    main()
