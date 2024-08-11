import unittest
from unittest.mock import patch, MagicMock
from task_automation_bot import NotificationSender

class TestNotificationSending(unittest.TestCase):

    def setUp(self):
        self.notification_sender = NotificationSender()
  
    @patch('task_automation_bot.smtp_lib.send_email') 
    def test_send_email_notification(self, mock_send_email):
        mock_send_email.return_value = True
        result = self.notification_sender.send_email('test@mail.com', 'Hello', 'Test message')
        self.assertTrue(result)
        mock_send_email.assert_called_with('test@mail.com', 'Hello', 'Test message')

    @patch('task_automation_bot.SomeOtherLib.send_sms') 
    def test_send_sms_notification(self, mock_send_sms):
        mock_send_sms.return_value = True
        result = self.notification_sender.send_sms('123456789', 'SMS Test message')
        self.assertTrue(result)
        mock_send_sms.assert_called_with('123456789', 'SMS Test message')

    @patch('task_automation_bot.slack_sdk.WebClient.chat_postMessage')
    def test_send_slack_notification(self, mock_slack):
        mock_slack.return_value = {'ok': True}
        result = self.notification_sender.send_slack_message('channel_id', 'Slack Test message')
        self.assertTrue(result)
        mock_slack.assert_called_with(channel='channel_id', text='Slack Test message')

    @patch.dict('os.environ', {'API_KEY': 'test_api_key'})
    @patch('task_automation_bot.SomeAPI.send_notification') 
    def test_send_api_notification(self, mock_api_notification):
        mock_api_notification.return_value = True
        result = self.notification_sender.send_api_notification('user_id', 'API Test message')
        self.assertTrue(result)
        mock_api_notification.assert_called_with('user_id', 'API Test message')

if __name__ == '__main__':
    unittest.main()