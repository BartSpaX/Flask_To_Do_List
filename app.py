from flask import Flask, render_template, request, jsonify, redirect, url_for
# from flask_restful import Api
from models import db, Task
# from routes import TaskListResource, TaskResource

app = Flask(__name__)
# api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    # tasks = Task.query.all()
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = Task(title=data["title"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title, "done": new_task.done})

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"})
    data = request.get_json()
    task.done = data["done"]
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done})
        

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"})
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(debug=True)