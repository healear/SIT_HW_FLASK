from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource



DATABASE_NAME = 'todo.sqlite'
engine = create_engine(f'sqlite:///{DATABASE_NAME}')
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

def create_base():
    Base.metadata.create_all(engine)