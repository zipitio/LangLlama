from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String(50), unique = True)
    genre = Column(String(50))