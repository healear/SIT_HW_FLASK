import os.path

from flask import Flask, jsonify
from DB_Model import DATABASE_NAME, session
from data.user import User

import create_db

app = Flask(__name__)


@app.route("/")
def home():
    return {"message": "Fine"}, 200


@app.route("/users")
def get_users():
    return jsonify(
        [
            {"id": user.id, "name": user.name, "password": user.password}
            for user in User.querry.all()
        ]
    )


if __name__ == "__main__":
    db_created_check = os.path.exists(DATABASE_NAME)
    if not db_created_check:
        create_db.create_base()

    _session = session()
