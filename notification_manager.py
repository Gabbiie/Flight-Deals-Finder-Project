from twilio.rest import Client
import smtplib
from dotenv import load_dotenv
import os

load_dotenv(".env")

ACC_SID = os.getenv("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_NUM = os.getenv("TWILIO_NUMBER")
RECEIVING_NUM = os.getenv("RECEIVING_NUMBER")
EMAIL_ADDR = os.getenv("EMAIL")
MY_PASSWORD = os.getenv("PASSWORD")


class NotificationManager:
    def __init__(self):
        self.client = Client(ACC_SID, TWILIO_AUTH_TOKEN)

    def send_text(self, msg):
        """Send text message with flight information"""
        client = Client(ACC_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
                    body=msg,
                    from_=TWILIO_NUM,
                    to=RECEIVING_NUM
                    )

        return message.status

    def send_emails(self, message, emails_list):
        """Send email with flight information"""
        with smtplib.SMTP("smtp.gmail.com") as connection:

            connection.starttls()
            connection.login(user=EMAIL_ADDR, password=MY_PASSWORD)

            for email in emails_list:
                connection.sendmail(from_addr=EMAIL_ADDR,
                                    to_addrs=email,
                                    msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8'))
                print("Email sent!")
