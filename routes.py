from flask import Flask, jsonify, request
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/task', methods=['POST'])
def create_task():
    data = request.get_json()
    return jsonify({'message': 'Task created successfully!'}), 201

@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    return jsonify({'message': 'Task updated successfully!'}), 200

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    return jsonify({'message': 'Task deleted successfully!'}), 200

@app.route('/settings/notifications', methods=['POST'])
def update_notifications():
    data = request.get_json()
    return jsonify({'message': 'Notification settings updated successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)