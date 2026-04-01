from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)
FILE_NAME = "tasks.txt"

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return [t for t in f.read().splitlines() if t.strip()]

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        for task in tasks:
            f.write(task + "\n")

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    task = data.get("task", "").strip()
    if not task:
        return jsonify({"error": "Empty task"}), 400
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return jsonify({"message": "Task added", "tasks": tasks})

@app.route("/tasks/<int:index>", methods=["DELETE"])
def delete_task(index):
    tasks = load_tasks()
    if index < 0 or index >= len(tasks):
        return jsonify({"error": "Invalid index"}), 400
    removed = tasks.pop(index)
    save_tasks(tasks)
    return jsonify({"message": f"Deleted: {removed}", "tasks": tasks})

if __name__ == "__main__":
    app.run(debug=True)