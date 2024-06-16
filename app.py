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
        to_remove = []
        for task_id in scheduled_tasks.keys():
            task = scheduled_tasks[task_id]
            if task['execute']:
                try:
                    task['function']()  
                    task['execute'] = False  
                finally:
                    to_remove.append(task_id)
        for task_id in to_remove:
            del scheduled_tasks[task_id]
        sleep(60)  

def example_task():
    print("Task executed")

@app.route('/schedule_task', methods=['POST'])
def schedule_task():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"message": "Invalid or missing JSON in request"}), 400

    task_id = data.get('task_id')
    task_name = data.get('task_name')

    # Validate task_id and task_name presence
    if not task_id or not task_name:
        return jsonify({"message": "Missing task_id or task_name"}), 400

    if task_id in scheduled_tasks:
        return jsonify({"message": "Task with this ID is already scheduled", "task_id": task_id}), 400

    if task_name == "example_task":
        scheduled_tasks[task_id] = {'function': example_task, 'execute': True}
        return jsonify({"message": "Task scheduled", "task_id": task_id}), 200
    else:
        return jsonify({"message": "Task not found", "task_id": task_id}), 404

if __name__ == '__main__':
    scheduler_thread = Thread(target=task_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", 5000)))