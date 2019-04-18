from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

tasks = {
    1: "買い物",
    2: "映画鑑賞",
    3: "レポート作成"
}


@app.route("/tasks", methods=["GET"])
def list_all_tasks():
    """
    $ curl localhost:5000/tasks
    {
      "message": {
        "1": "買い物",
        "2": "映画鑑賞",
        "3": "レポート作成"
      }
    }
    """
    json = {
        "message": tasks
    }
    return jsonify(json)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def show_task(task_id: int):
    """
    $ curl  localhost:5000/tasks/1
    {
      "message": "買い物"
    }
    """
    if task_id in tasks.keys():
        message = tasks[task_id]
    else:
        message = f"Task {task_id} is not exists in tasks"

    json = {
        "message": message
    }
    return jsonify(json)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    """
    $ curl -X DELETE localhost:5000/tasks/1
    {
      "message": "Task 1 deleted"
    }

    $ curl -X DELETE localhost:5000/tasks/999
    {
      "message": "Task 999 is not exists in tasks"
    }
    """
    if task_id in tasks.keys():
        del tasks[task_id]
        message = f"Task {task_id} deleted"
    else:
        message = f"Task {task_id} is not exists in tasks"

    json = {
        "message": message
    }

    return jsonify(json)


@app.route("/tasks", methods=["POST"])
def create_task():
    """
    $ curl -X POST
           -H 'Content-Type:application/json'
           -d '{"task": "ジムに行く"}'
           localhost:5000/tasks
    {
      "message": "New task created"
    }
    """
    # id連番じゃないよ
    task_id = max(tasks.keys()) + 1

    posted = request.get_json()

    if "task" in posted:
        tasks[task_id] = posted["task"]
        msg = "New task created"
    else:
        msg = "No task created"

    json = {"message": msg}

    return jsonify(json)


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    """
    $ curl -X PUT
           -H 'Content-Type:application/json'
           -d '{"task": "ジムに行く"}'
           localhost:5000/tasks/1
    {
      "message": "Task 1 updated"
    }

    $ curl -X PUT
           -H 'Content-Type:application/json'
           -d '{"task": "ジムに行く"}'
           localhost:5000/tasks/999
    {
      "message": "No task updated"
    }
    """
    posted = request.get_json()

    if 'task' in posted and task_id in tasks.keys():
        tasks[task_id] = posted['task']
        msg = 'Task {} updated'.format(task_id)
    else:
        msg = 'No task updated'

    json = {
        'message': msg
    }
    return jsonify(json)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
