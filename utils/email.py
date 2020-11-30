import smtplib
from email.mime.text import MIMEText

from utils.logging import logger
from settings import (
    email_sender,
    email_password,
    email_recipients,
)


def email(item_name, item_url="", subject=None, body=None):
    email_subject = f"*** ITEM ({item_name}) ADDED TO YOUR CART ***"
    email_body = f"Item ({item_name}) has been added to your cart. Hurry login to buy it now: https://newegg.com\n\n item url: {item_url}"

    msg = MIMEText(body or email_body)
    msg["Subject"] = subject or email_subject
    msg["From"] = email_sender
    msg["To"] = ", ".join(email_recipients)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo
        server.login(email_sender, email_password)
        server.sendmail(from_addr=email_sender, to_addrs=email_recipients, msg=msg.as_string())
        server.quit()
        logger.info(f"Successfully sent out email notification for ({item_name})")
    except Exception as e:
        logger.exception("something went wrong trying to send an email...")
        logger.exception(e)
        print("something went wrong trying to send an email...")
