from faker import Faker
from DB_Model import create_base, session
from data.todo import Todo
from data.user import User
from data.uploads import File

def create_database(load_fake_data: bool=True):
    create_base()
    if load_fake_data:
        _load_fake_data(session())


def _load_fake_data(_session: session):
    user = User(name='Vasya',password='example')
    _session.add(user)
    todos = ['Eat','Sleep','Fortnite','Repeat']
    for key, it in enumerate(todos):
        todo = Todo(name=it)
        todo.user_id.append(user.id)
        _session.add(todo)
    faker = Faker()