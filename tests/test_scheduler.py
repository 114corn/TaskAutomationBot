import unittest
from unittest.mock import patch
from task_scheduler import TaskScheduler
import os

class TestTaskScheduler(unittest.TestCase):

    def setUp(self):
        self.api_key = os.getenv("API_KEY", "default_api_key")
        self.scheduler = TaskScheduler(api_key=self.api_key)
        
    def test_schedule_task_successfully(self):
        scheduled_time = "2023-07-10 10:00:00"
        task_identifier = "SampleTask"
        self.assertTrue(self.scheduler.schedule_task(scheduled_time, task_identifier))
    
    @patch('task_scheduler.TaskScheduler.schedule_task')
    def test_mock_scheduling_task(self, mock_schedule_task):
        scheduled_time = "2023-07-12 12:00:00"
        task_identifier = "MockedTask"
        mock_schedule_task.return_value = True
        execution_result = self.scheduler.schedule_task(scheduled_time, task_identifier)
        self.assertTrue(execution_result)
        mock_schedule_task.assert_called_once_with(scheduled_time, task_identifier)

    def test_invalid_time_raises_error(self):
        invalid_time = "invalid_time"
        task_identifier = "TaskWithInvalidTime"
        with self.assertRaises(ValueError):
            self.scheduler.schedule_task(invalid_time, task_identifier)
    
    def test_unavailable_slot_raises_exception(self):
        scheduled_time = "2023-12-25 13:00:00"
        task_identifier = "NewYearPrep"
        with self.assertRaises(self.scheduler.SlotUnavailableException):
            self.scheduler.schedule_task(scheduled_time, task_identifier)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()