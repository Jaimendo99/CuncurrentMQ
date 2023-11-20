import config
from email.message import EmailMessage
import ssl
import smtplib


def send_email(subject, body, to_email):
    em = EmailMessage()
    em['Subject'] = subject
    em['From'] = config.sender
    em['To'] = to_email
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(config.sender, config.passcode)
        smtp.sendmail(config.sender, to_email, em.as_string())

    return True
