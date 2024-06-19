from flask import Flask, request, jsonify
import os
from threading import Thread
from time import sleep
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

tasks_schedule = {}

def run_scheduled_tasks():
    while True:
        completed_tasks = []
        for task_id, task_details in tasks_schedule.items():
            if task_details['is_scheduled']:
                try:
                    task_details['task_function']()  
                    task_details['is_scheduled'] = False  
                finally:
                    completed_tasks.append(task_id)
        for task_id in completed_tasks:
            del tasks_schedule[task_id]
        sleep(60)  

def perform_example_task():
    print("Example task executed")

@app.route('/schedule_task', methods=['POST'])
def handle_task_scheduling():
    request_data = request.get_json(force=True, silent=True)
    if not request_data:
        return jsonify({"message": "Invalid or missing JSON in request"}), 400

    task_id = request_data.get('task_id')
    task_name = request_data.get('task_name')

    if not task_id or not task_name:
        return jsonify({"message": "Missing task_id or task_name"}), 400

    if task_id in tasks_schedule:
        return jsonify({"message": "Task with this ID is already scheduled", "task_id": task_id}), 400

    if task_name == "example_task":
        tasks_schedule[task_id] = {'task_function': perform_example_task, 'is_scheduled': True}
        return jsonify({"message": "Task successfully scheduled", "task_id": task_id}), 200
    else:
        return jsonify({"message": "Specified task not found", "task_id": task_id}), 404

if __name__ == '__main__':
    task_scheduler_thread = Thread(target=run_scheduled_tasks, daemon=True)
    task_scheduler_thread.start()
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", 5000)))