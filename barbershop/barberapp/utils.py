# /workspace/Barbershop/barbershop/barberapp/utils.py

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from django.conf import settings

def send_email(to_email, subject, content):
    sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    email = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )
    try:
        response = sg.send(email)
        return response.status_code
    except Exception as e:
        print(e)
        return None

def send_sms(to_phone, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        return message.sid
    except Exception as e:
        print(e)
        return None
