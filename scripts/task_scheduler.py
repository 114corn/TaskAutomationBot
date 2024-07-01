import schedule
import time
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def make_api_call(data):
    print("API call made with data:", data)
    return {"success": True, "data": data}

def batch_api_calls(tasks_data):
    consolidated_response = []
    for task_data in tasks_data:
        response = make_api_call(task_data)
        consolidated_response.append(response)
    print("Batch API call completed.")
    return consolidated_response

def task1():
    print("Executing Task 1")
    return {"task": "1", "data": "Some data for Task 1"}

def task2():
    print("Executing Task 2")
    return {"task": "2", "data": "Some data for Task 2"}

def schedule_tasks():
    task1_interval = int(os.getenv('TASK1_INTERVAL', 10))
    schedule.every(task1_interval).minutes.do(lambda: task_queue.append(task1()))
    
    task2_time = os.getenv('TASK2_TIME', '12:00')
    schedule.every().day.at(task2_time).do(lambda: task_queue.append(task2()))

def run_scheduler():
    print("Task scheduler started...")
    global task_queue
    task_queue = []
    while True:
        schedule.run_pending()
        if task_queue:
            batch_api_calls(task_queue)
            task_queue.pop(0)
        time.sleep(1)

if __name__ == "__main__":
    schedule_tasks()
    run_neighbors()