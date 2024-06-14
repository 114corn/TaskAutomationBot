from flask import Flask, request, jsonify
import os
from threading import Thread
from time import sleep
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

scheduled_tasks = {}

def task_scheduler():
    while True:
        for task_id in list(scheduled_tasks.keys()):
            task = scheduled_tasks[task_id]
            if task['execute']:
                task['function']()  
                task['execute'] = False  
                del scheduled_tasks[task_id]
        sleep(60)  

def example_task():
    print("Task executed")

@app.route('/schedule_task', methods=['POST'])
def schedule_task():
    data = request.get_json()
    task_id = data.get('task_id')
    task_name = data.get('task_name')
    if task_name == "example_task":
        scheduled_tasks[task_id] = {'function': example_task, 'execute': True}
        return jsonify({"message": "Task scheduled", "task_id": task_id}), 200
    else:
        return jsonify({"message": "Task not found", "task_id": task_id}), 404

if __name__ == '__main__':
    scheduler_thread = Thread(target=task_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=os.environ.get("PORT", 5000))