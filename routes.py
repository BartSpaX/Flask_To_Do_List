from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import db, Task

class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])

    def post(self):
        data = request.get_json()
        new_task = Task(title=data["title"])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"id": new_task.id, "title": new_task.title, "done": new_task.done})

class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get(task_id)
        if task:
            return jsonify({"id": task.id, "title": task.title, "done": task.done})
        return {"message": "Task not found"}, 404

    def put(self, task_id):
        task = Task.query.get(task_id)
        if task:
            data = request.get_json()
            task.title = data.get("title", task.title)
            task.done = data.get("done", task.done)
            db.session.commit()
            return jsonify({"id": task.id, "title": task.title, "done": task.done})
        return {"message": "Task not found"}, 404

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return {"message": "Task deleted"}
        return {"message": "Task not found"}, 404

