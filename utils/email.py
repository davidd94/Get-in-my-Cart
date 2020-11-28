import smtplib
from email.mime.text import MIMEText
import os

from settings import (
    email_options,
    email_subject,
    email_body,
)


cur_dir = os.getcwd()


def email(subject=None, body=None):
    sender_email = email_options["email"]
    sender_pass = email_options["password"]
    recipients = email_options["recipients"]

    msg = MIMEText(body or email_body)

    msg["Subject"] = subject or email_subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo
        server.login(sender_email, sender_pass)
        server.sendmail(from_addr=sender_email, to_addrs=recipients, msg=msg.as_string())
        server.quit()
    except:
        print("something went wrong")
    
