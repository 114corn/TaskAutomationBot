import unittest
from task_automation_bot import TaskAutomationBot
from unittest.mock import patch, Mock
from os import environ

API_KEY = environ.get("API_KEY")
SAMPLE_TASK_NAME = environ.get("SAMPLE_TASK")
INVALID_TASK_NAME = environ.get("INVALID_TASK")

class TestTaskAutomationBot(unittest.TestCase):

    def setUp(self):
        self.taskBot = TaskAutomationBot(api_key=API_KEY)

    @patch('task_automation_bot.TaskAutomationBot.execute_task')
    def test_execute_valid_task_successfully(self, mock_execute_task):
        mock_execute_task.return_value = True

        execution_result = self.taskBot.execute_task(SAMPLE_TASK_NAME)
        
        self.assertTrue(execution_result)
        mock_execute_task.assert_called_once_with(SAMPLE_TASK_NAME)

    @patch('task_automation_bot.TaskAutomationBot.execute_task')
    def test_execute_invalid_task_fails(self, mock_execute_task):
        mock_execute_task.return_value = False

        execution_result = self.taskBot.execute_task(INVALID_TASK_NAME)
        
        self.assertFalse(execution_result)
        mock_execute_task.assert_called_once_with(INVALID_TASK_NAME)

    @patch('task_automation_bot.TaskAutomationBot.fetch_task_result')
    def test_fetch_result_for_valid_task(self, mock_fetch_task_result):
        expected_task_completion_message = "Task completed successfully"
        mock_fetch_task_result.return_value = expected_task_completion_message

        actual_result = self.taskBot.fetch_task_result(SAMPLE_TASK_NAME)

        self.assertEqual(actual_result, expected_task_completion_message)
        mock_fetch_task_result.assert_called_once_with(SAMPLE_TASK_NAME)

    @patch('task_automation_bot.TaskAutomationBot.fetch_task_result')
    def test_fetch_result_for_invalid_task(self, mock_fetch_task_result):
        expected_error_message = "Error: Task not found"
        mock_fetch_task_result.return_value = expected_error_message

        actual_result = self.taskBot.fetch_task_result(INVALID_TASK_NAME)

        self.assertEqual(actual_result, expected_error_message)
        mock_fetch_task_result.assert_called_once_with(INVALID_TASK_NAME)

if __name__ == '__main__':
    unittest.main()