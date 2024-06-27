import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()

def task1():
    print("Executing Task 1")

def task2():
    print("Executing Task 2")

def schedule_tasks():
    task1_interval = int(os.getenv('TASK1_INTERVAL', 10))
    schedule.every(task1_interval).minutes.do(task1)
    task2_time = os.getenv('TASK2_TIME', '12:00')
    schedule.every().day.at(task2_time).do(task2)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_tasks()
    print("Task scheduler started...")
    runariant_scheduler()