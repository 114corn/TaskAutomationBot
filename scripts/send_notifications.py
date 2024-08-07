import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from twilio.rest import Client
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(filename="notification_manager_log.txt", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

class NotificationManager:
    def __init__(self):
        self.email_server = self.setup_email_server()
        self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    @staticmethod
    def setup_email_server():
        try:
            server = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            logging.info("Email server initiated successfully")
            return server
        except Exception as e:
            logging.error(f"Failed to initiate email server: {e}")
            return None

    def send_email(self, to_email, subject, message):
        if self.email_server:
            try:
                email = MIMEMultipart()
                email['From'] = EMAIL_HOST_USER
                email['To'] = to_email
                email['Subject'] = subject
                email.attach(MIMEText(message, 'plain'))

                self.email_server.send_message(email)
                logging.info(f"Email sent successfully to {to_email}")
            except Exception as e:
                logging.error(f"Failed to send email to {to_email}: {e}")
        else:
            logging.warning("Email server is not available.")

    def send_sms(self, to_phone_number, message):
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=to_phone_number
            )
            logging.info(f"SMS sent successfully to {to_phone_number}")
        except Exception as e:
            logging.error(f"Failed to send SMS to {to_phone_number}: {e}")

    def close_email_server(self):
        if self.email_server:
            self.email_server.quit()
            logging.info("Email server connection closed.")

if __name__ == "__main__":
    notification_manager = NotificationManager()
    task_completed = True
    if task_completed:
        notification_manager.send_email("example@example.com", "Task Completed", "Hey, your task is now complete.")
        notification_manager.send_sms("+1234567890", "Hey, your task is now complete.")
    notification_manager.close_email_server()