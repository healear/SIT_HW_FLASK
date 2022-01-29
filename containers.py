from dependency_injector import containers
from service import Service
from dotenv import dotenv_values

class Container(containers.DeclarativeContainer):
    config = dotenv_values(".flaskenv")["FLASK_ENV"]
    service = Service(f"{config}")