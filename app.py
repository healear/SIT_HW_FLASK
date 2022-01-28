import uuid

from flask import Flask, request, jsonify, send_file
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from io import BytesIO
import jwt

import DB_Model
from data.user import User
from data.todo import Todo
from data.uploads import File
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from DB_Model import *
from functools import wraps

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
app.config["UPLOAD_FOLDER"] = "/uploads/"
_session = SQLAlchemy(app)
_secret = "\x87\xdb\xcd\xf5\rd\x0bF@\x92\x17\x95A\x10\x85X\x15O\x1d\xa8\xd496\xe6"


def get_token(_payload):
    token = jwt.encode(payload={"username": _payload}, key=_secret, algorithm="HS256")
    return token


def authorize(username, password):
    u = _session.session.query(User).filter(User.username == username).first()
    if not password == u.password:
        raise Exception("Wrong password")
    return u


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].strip("Bearer").strip()
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, _secret, algorithms="HS256")
            u = (
                _session.session.query(User)
                .filter(User.username == data["username"])
                .first()
            )
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users contex to the routes
        return f(u, *args, **kwargs)

    return decorated


@app.route("/uploads", methods=["POST"])
def upload_file():
    file = request.files["upload"]
    data = file.read()
    size = str(len(data)) + "bytes"
    new_file = File(file.filename, size, data)
    _session.session.add(new_file)
    _session.session.commit()
    return {"message": "Upload succful"}


@app.route("/uploads", methods=["GET"])
def get_file_list():
    qfiles = _session.session.query(File)
    files = []
    for file in qfiles:
        files.append({"id": file.id, "name": file.name, "size": file.size})
    return jsonify(files), 200


@app.route("/download/<string:name>", methods=["GET"])
def download_file(name):
    file = _session.session.query(File).filter(File.name == name).first()
    if not file:
        return {"error": "No file with this name was found"}
    return send_file(
        BytesIO(file.data), attachment_filename=f"{name}", as_attachment=True
    )


@app.route("/uploads/<string:name>", methods=["DELETE"])
def delete_file(name):
    file = _session.session.query(File).filter(File.name == name).first()
    if not file:
        return {"error": "No file with this name was found"}
    _session.session.delete(file)
    _session.session.commit()
    return {"message": "Delete succful"}


@app.route("/login", methods=["POST"])
def authorisation():
    if request.method == "POST":
        data = request.get_json()
        if not "username" in data or not "password" in data:
            return (
                jsonify(
                    {
                        "error": "Bad request",
                        "message": "Usename or password is not given",
                    }
                ),
                400,
            )
        if len(data["username"]) < 4 or len(data["password"]) < 4:
            return (
                jsonify(
                    {
                        "error": "Bad request",
                        "message": "Name and password must be contain minimum of 4 letters",
                    }
                ),
                400,
            )
        username = data["username"]
        password = data["password"]
        users = authorize(username, password)
        token = get_token(users.username)
        return jsonify({"token": token}), 200
    return jsonify({"error": "Wrong request type"}), 400


@app.route("/reg", methods=["POST"])
def registrate():
    data = request.get_json()
    if not "username" in data or not "password" in data:
        return (
            jsonify(
                {"error": "Bad request", "message": "Usename or password is not given"}
            ),
            400,
        )
    if len(data["username"]) < 4 or len(data["password"]) < 4:
        return (
            jsonify(
                {
                    "error": "Bad request",
                    "message": "Name and password must be contain minimum of 4 letters",
                }
            ),
            400,
        )
    u = User(
        username=data["username"],
        password=data["password"],
    )
    _session.session.add(u)
    _session.session.commit()
    return {"id": u.id, "username": u.username}, 201


@app.route("/todo", methods=["POST", "GET"])
@token_required
def todo(curr_u):
    """GET AND POST USER TODO"""
    if request.method == "POST":
        data = request.get_json()
        new_todo = Todo(name=data["name"], userid=curr_u.id)
        _session.session.add(new_todo)
        _session.session.commit()
        return {"message": "Todo added"}
    if request.method == "GET":
        info = _session.session.query(Todo).filter(Todo.user_id == curr_u.id)
        todos = []
        for item in info:
            todos.append({"name": item.name})
        return jsonify(todos), 200
    return {"Error": "Check request method"}


@app.route("/todo/<string:name>", methods=["PUT", "DELETE"])
@token_required
def todo_change(curr_u, name):
    """DELETE AND PUT TODO"""
    if request.method == "PUT":
        info = (
            _session.session.query(Todo)
            .filter(Todo.user_id == curr_u.id, Todo.name == name)
            .first()
        )
        data = request.get_json()
        new_name = data["name"]
        if not info:
            resp = jsonify({"message": "No item with this id"}), 400
            return resp
        info.name = new_name
        _session.session.commit()
        return {"message": "Update succful"}
    if request.method == "DELETE":
        info = (
            _session.session.query(Todo)
            .filter(Todo.user_id == curr_u.id, Todo.name == name)
            .first()
        )
        if not info:
            resp = jsonify({"message": "No item with this id"}), 400
            return resp
        _session.session.delete(info)
        _session.session.commit()
        return {"message": "Delete succful"}
    return {"Error": "Check request method"}


api = Api(app)
