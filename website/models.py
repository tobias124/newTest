from lib2to3.pytree import Base
from flask_login import UserMixin
from sqlalchemy import *
from . import db

# assoc. table between player and game for payments
participates = db.Table('participates',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('bet_is_payed', db.Boolean, default=False)
)

# User
class Player(UserMixin, db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    role = db.Column(db.String(20))
    bets = db.relationship('Bet') # 1 to Many Relation
    paying = db.relationship('Game', secondary = participates, backref='payers')
    # PLAYER AND GAME REL

    def __init__(self, **kwargs):
      super().__init__(**kwargs)


# Game
class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gameday = db.Column(db.Integer)
    home_team = db.Column(db.String(200))
    away_team = db.Column(db.String(200))
    home_goals = db.Column(db.Integer)
    away_goals = db.Column(db.Integer)
    enabled = db.Column(db.Boolean)
    bets = db.relationship('Bet') # 1 to Many Relation

    def __init__(self, **kwargs):
       super().__init__(**kwargs)


#Bet
class Bet(db.Model):
    __tablename__ = 'bet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    home_goals = db.Column(db.Integer)
    away_goals = db.Column(db.Integer)
    participant = db.Column(db.String(20))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', ondelete="CASCADE"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


