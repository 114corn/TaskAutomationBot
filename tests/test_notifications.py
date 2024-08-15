import unittest
from unittest.mock import patch, MagicMock
from task_automation_bot import NotificationSender
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

class NotificationSender:
    def send_email(self, receiver_email, subject, body):
        try:
            logger.info(f"Sending email to {receiver_email} with subject: '{subject}'")
            logger.info("Email sent successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise e

class TestNotificationSending(unittest.TestCase):

    def setUp(self):
        self.notification_sender = NotificationSender()
  
    @patch('task_automation_bot.smtp_lib.send_email') 
    def test_send_email_notification(self, mock_send_email):
        mock_send_email.return_value = True
        result = self.notification_sender.send_email('test@mail.com', 'Hello', 'Test message')
        self.assertTrue(result)
        mock_send_email.assert_called_with('test@mail.com', 'Hello', 'Test message')
        
        mock_send_email.side_effect = Exception("Failed to send email")
        with self.assertRaises(Exception) as context:
            self.notification_sender.send_email('test@mail.com', 'Hello', 'Test message')
        self.assertTrue('Failed to send email' in str(context.exception))

    @patch('task_automation_bot.SomeOtherLib.send_sms') 
    def test_send_sms_notification(self, mock_send_sms):
        mock_send_sms.return_value = True
        result = self.notification_sender.send_sms('123456789', 'SMS Test message')
        self.assertTrue(result)
        
        mock_send_sms.side_effect = Exception("Failed to send SMS")
        with self.assertRaises(Exception) as context:
            self.notification_sender.send_sms('123456789', 'SMS Test message')
        self.assertTrue('Failed to send SMS' in str(context.exception))

    @patch('task_automation_bot.slack_sdk.WebClient.chat_postMessage')
    def test_send_slack_notification(self, mock_slack):
        mock_slack.return_value = {'ok': True}
        result = self.notification_sender.send_slack_message('channel_id', 'Slack Test message')
        self.assertTrue(result)
        
        mock_slack.side_effect = Exception("Failed to send Slack message")
        with self.assertRaises(Exception) as context:
            self.notification_sender.send_slack_message('channel_id', 'Slack Test message')
        self.assertTrue('Failed to send Slack message' in str(context.exception))

    @patch.dict('os.environ', {'API_KEY': 'test_api_key'})
    @patch('task_automation_bot.SomeAPI.send_notification') 
    def test_send_api_notification(self, mock_api_notification):
        mock_api_notification.return_value = True
        result = self.notification_sender.send_api_notification('user_id', 'API Test message')
        self.assertTrue(result)
        
        mock_api_notification.side_effect = Exception("Failed to send API notification")
        with self.assertRaises(Exception) as context:
            self.notification_sender.send_api_notification('user_id', 'API Test message')
        self.assertTrue('Failed to send API notification' in str(context.exception))

if __name__ == '__main__':
    unittest.main()