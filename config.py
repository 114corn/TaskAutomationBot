import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SCHEDULER_TIMEZONE = os.getenv('SCHEDULER_TIMEZONE', 'UTC')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL = os.getenv('EMAIL')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER')
    DB_URI = os.getenv('DB_URI', 'sqlite:///tasks.db')
