from twilio.rest import Client
import smtplib

ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
AUTH_TOKEN = "YOUR_TWILIO_ACCOUNT_AUTH_TOKEN"
TWILIO_PHONE_NUM = ""
# Assuming you use gmail, if not search for your email provider smtp address and insert below
EMAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"
MY_EMAIL = ""
MY_PASSWORD = ""
MY_PHONE_NUM = ""


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_msg(self, msg):
        message = self.client.messages.create(
            body=msg,
            from_=TWILIO_PHONE_NUM,
            to=MY_PHONE_NUM,
        )
        print(message.sid)

    def send_emails(self, emails, google_flight_link, message):
        with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )
