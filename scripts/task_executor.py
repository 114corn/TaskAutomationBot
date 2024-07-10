import schedule
import time
import subprocess
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

@lru_cache(maxsize=None)
def send_email():
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')  # Fix variable name consistency
    password = os.getenv('EMAIL_PASSWORD')  # Fix variable name consistency

    message = MIMEMultipart("alternative")
    message["Subject"] = "Scheduled Email"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Hi,
    How are you?
    This is a scheduled email."""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <b>This is a scheduled email.</b>
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')), context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        print("Error sending email: ", e)

@lru_cache(maxsize=None)
def run_script():
    try:
        subprocess.run(['python', 'path/to/your/script.py'], check=True)
    except subprocess.CalledProcessError as e:
        print("The script execution failed: ", e)

schedule.every().day.at("10:30").do(send_email)
schedule.every().monday.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)