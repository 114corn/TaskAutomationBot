import unittest
from unittest.mock import patch
from task_scheduler import TaskScheduler
import os

class TestTaskScheduling(unittest.TestCase):

    def setUp(self):
        self.some_api_key = os.getenv("SOME_API_KEY", "default_api_key")
        self.scheduler = TaskScheduler(api_key=self.some_api_key)
        
    def test_schedule_task_correctly(self):
        task_time = "2023-07-10 10:00:00"
        task_name = "SampleTask"
        self.assertTrue(self.scheduler.schedule_task(task_time, task_name))
    
    @patch('task_scheduler.TaskScheduler.schedule_task')
    def test_schedule_task_with_mock(self, mock_schedule_task):
        task_time = "2023-07-12 12:00:00"
        task_name = "MockedTask"
        mock_schedule_task.return_value = True
        result = self.scheduler.schedule_task(task_time, task_name)
        self.assertTrue(result)
        mock_schedule_task.assert_called_once_with(task_time, task_name)

    def test_handle_invalid_time(self):
        task_time = "invalid_time"
        task_name = "TaskWithInvalidobtime"
        with self.assertRaises(ValueError):
            self.scheduler.schedule_task(task_time, task_name)
    
    def test_handling_unavailable_slots(self):
        task_time = "2023-12-25 13:00:00"
        task_name = "NewYearPrep"
        with self.assertRaises(self.scheduler.SlotUnavailableException):
            self.scheduler.schedule_task(task_time, task_name)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()