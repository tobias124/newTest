from . import db

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    shirt_number = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)

    def __init__(self, first_name, last_name, password, shirt_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.shirt_number = shirt_number
        self.email = email
