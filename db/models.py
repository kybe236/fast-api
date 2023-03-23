from sqlalchemy import Column, Integer, String

from .database import Base


class Games(Base):
    __tablename__ = "games"

    game_code = Column(String, primary_key=True, index=True)
    player1_win = Column(Integer)
    player2_win = Column(Integer)
    last_winner = Column(Integer)
