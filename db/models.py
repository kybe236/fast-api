from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class Game(Base):
    __tablename__ = "users"

    code = Column(Integer, unique=True, primary_key=True)
    player1 = Column(Integer, default=0)
    player2 = Column(Integer, default=0)
    last_winner = Column(Integer, default=-1)
