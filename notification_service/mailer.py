import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "m25ai1018@iitj.ac.in"
SMTP_PASS = "dwtaisvyvipdenqs"  

def send_welcome_email(to: str, name: str):
    subject = "Welcome to Bookstore!"
    body = f"""
    Hello {name},

    Welcome to our bookstore platform! 🎉
    Your account is now active.

    If you need assistance, reply to this email.

    Regards,
    Bookstore Team
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to, msg.as_string())
