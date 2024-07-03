import schedule
import time
import os
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def make_api_call(data):
    print("API call made with data:", data)
    # Simulate a real API call
    return {"success": True, "data": data}

def batch_api_calls(tasks_data):
    consolidated_response = []
    for task_data in tasks_stored_here:
        response = make_api_call(task_data)
        consolidated_response.append(response)
    print("Batch API call completed.")
    # Log the results of the batch call
    log_results(consolidated_response)
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

def log_results(results):
    """
    Logs the outcome of batch_api_calls to a file.
    """
    with open('task_automation_log.txt', 'a') as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{timestamp} - Batch Results: {results}\n")
        print("Results logged.")

def run_scheduler():
    print("Task scheduler started...")
    global task_queue
    task_queue = []
    while True:
        schedule.run_pending()
        if task_queue:
            batch_api_calls(task_queue)
            # Corrected logic to clear the task queue after processing
            task_queue.clear()
        time.sleep(1)

if __name__ == "__main__":
    schedule_tasks()
    run_gscheduler()