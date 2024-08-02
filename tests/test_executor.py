import unittest
from task_automation_bot import TaskAutomationBot
from unittest.mock import patch, Mock
from os import environ

API_KEY = environ.get("API_KEY")
SAMPLE_TASK = environ.get("SAMPLE_TASK")
INVALID_TASK = environ.get("INVALID_TASK")

class TestTaskAutomationBot(unittest.TestCase):

    def setUp(self):
        self.bot = TaskAutomationBot(api_key=API_KEY)

    @patch('task_automation_bot.TaskAutomationBot.run_task')
    def test_run_valid_task(self, mock_run_task):
        mock_run_task.return_value = True

        result = self.bot.run_task(SAMPLE_TASK)
        
        self.assertTrue(result)
        mock_run_task.assert_called_once_with(SAMPLE_TASK)

    @patch('task_automation_bot.TaskAutomationBot.run_task')
    def test_run_invalid_task(self, mock_run_task):
        mock_run_task.return_value = False

        result = self.bot.run_task(INVALID_TASK)
        
        self.assertFalse(result)
        mock_run_task.assert_called_once_with(INVALID_TASK)

    @patch('task_automation_bot.TaskAutomationBot.get_task_result')
    def test_get_valid_task_result(self, mock_get_task_result):
        expected_result = "Task completed successfully"
        mock_get_task_result.return_value = expected_result

        result = self.bot.get_task_result(SAMPLE_TASK)

        self.assertEqual(result, expected_result)
        mock_get_task_result.assert_called_once_with(SAMPLE_TASK)

    @patch('task_automation_bot.TaskAutomationBot.get_task_result')
    def test_get_invalid_task_result(self, mock_get_task_result):
        expected_result = "Error: Task not found"
        mock_get_task_result.return_value = expected_result

        result = self.bot.get_task_result(INVALID_TASK)

        self.assertEqual(result, expected_result)
        mock_get_task_result.assert_called_once_with(INVALID_TASK)

if __name__ == '__main__':
    unittest.main()