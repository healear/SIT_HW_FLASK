from sqlalchemy import Column, Integer, String, ForeignKey
from data.user import User
from DB_Model import Base, session


class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))

    def __init__(self, name, userid):
        self.name = name
        self.user_id = userid

    def __repr__(self):
        info: str = f"Todo [Name: {self.name}]"
        return info

    def save(self):
        _session = session()
        _session.add(self)
        _session.commit()

    @staticmethod
    def get_all(user_id):
        return User.query.filter_by(created_by=user_id)

    def delete(self):
        _session = session
        _session.delete(self)
        _session.commit()
