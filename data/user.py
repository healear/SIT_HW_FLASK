from flask import Flask
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from DB_Model import Base, session
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    todo = relationship("Todo")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __int__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __repr__(self):
        info: str = f"User [Name: {self.username} Password: {self.password}]"
        return info

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        _session = session()
        _session.add(self)
        _session.commit()

    def generate_token(self, user_id):
        try:
            # set up a payload with an expiration time
            payload = {
                "exp": datetime.utcnow() + timedelta(minutes=5),
                "iat": datetime.utcnow(),
                "sub": user_id,
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload, app.config.get("SECRET"), algorithm="HS256"
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    def decode_token(token):
        try:
            payload = jwt.decode(token, app.config.get("SECRET"))
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
