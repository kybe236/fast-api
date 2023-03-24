from sqlalchemy import Column, Integer

from .database import Base


class Game(Base):
    __tablename__ = "games"

    code = Column(Integer, unique=True, primary_key=True)
    player1_score = Column(Integer, default=0)
    player2_score = Column(Integer, default=0)
    next_picker = Column(Integer, default=None)
    token1 = Column(Integer, default=None)
    token2 = Column(Integer, default=None)
    player1 = Column(Integer, default=None)
    player2 = Column(Integer, default=None)
