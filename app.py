from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import time # For a timestamp

app = Flask(__name__)
metrics = PrometheusMetrics(app) # This adds the /metrics endpoint

# In-memory "database"
todos = []
todo_id_counter = 0

# Helper function to find a todo by id
def find_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            return todo
    return None

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the SRE To-Do List API! Try /todos"}), 200

@app.route('/todos', methods=['POST'])
def add_todo():
    global todo_id_counter
    if not request.json or not 'task' in request.json:
        return jsonify({"error": "Task is required in JSON body"}), 400
    
    todo_id_counter += 1
    new_todo = {
        'id': todo_id_counter,
        'task': request.json['task'],
        'completed': False,
        'timestamp': time.time()
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = find_todo(todo_id)
    if todo:
        return jsonify(todo), 200
    return jsonify({"error": "Todo not found"}), 404

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    if not request.json:
        return jsonify({"error": "JSON body required"}), 400
    
    todo['task'] = request.json.get('task', todo['task'])
    todo['completed'] = request.json.get('completed', todo['completed'])
    return jsonify(todo), 200

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todo = find_todo(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({"message": "Todo deleted"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)