from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    genre = Column(String(50))
    platform = Column(String(50))
