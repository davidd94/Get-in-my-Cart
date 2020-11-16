import emails


async def send_email(email_address):
    message = emails.html(
        html=open("email_template.html"),
        subject="***ADDED A GPU IN YOUR NEWEGG CART***",
        mail_from=("Yourself", email_address)
    )

    response = message.send(
        to=email_address,
        smtp={"host": "David's email service", "port": 25}
    )

    print(response.status_code)
