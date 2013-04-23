from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Entry(Base):

    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return self.title

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username
