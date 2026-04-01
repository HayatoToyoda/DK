from flask import Flask, request, jsonify
import os

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "TODO App is running!", "tasks_count": len(tasks)})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    task = {"id": next_id, "title": data["title"], "done": False}
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "task not found"}), 404

    data = request.get_json()
    if "done" in data:
        task["done"] = data["done"]
    return jsonify(task)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
