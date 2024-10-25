from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(50))
    genre = Column(String(50))
