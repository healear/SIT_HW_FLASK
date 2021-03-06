from sqlalchemy import Column, Integer, String, LargeBinary
from DB_Model import Base


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    size = Column(String(30))
    data = Column(LargeBinary)

    def __init__(self, name, size, data):
        self.name = name
        self.size = size
        self.data = data

    def __repr__(self):
        info: str = f"File [Name: {self.name}, Size: {self.size}]"
        return info
