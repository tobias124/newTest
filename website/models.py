from flask_login import UserMixin
from . import db

# User
class Player(UserMixin, db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    shirt_number = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    role = db.Column(db.String(20))
    bets = db.relationship('Bet') # 1 to Many Relation

    def __init__(self, first_name, last_name, password, shirt_number, email, role):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.shirt_number = shirt_number
        self.email = email
        self.role = role


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


