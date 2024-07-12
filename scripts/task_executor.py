import schedule
import time
import subprocess
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

load_dotenv()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RETEIVER_EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')

ssl_context = ssl.create_default_context()

def send_email(sender_email=SENDER_EMAIL, receiver_email=RECEIVER_EMAIL, password=EMAIL_PASSWORD, smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT):
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
        with smtplib.SMTP_SSL(smtp_server, int(smtp_port), context=ssl_context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print("Error sending email: ", e)

def run_script(script_path='path/to/your/script.py'):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print("The script execution failed: ", e)

schedule.every().day.at("10:30").do(send_email)
schedule.every().monday.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)