import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .views import views

# init App
app = Flask(__name__)


def create_app(dev):
    if dev:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:SuperSecret@localhost/betgame'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oywafgwhonrxjc' \
                                                ':1fb26b2f767713170d4a21a7a92edcf077c34b0ebdc0f0ac5f2958005bdb35c0@ec2-52' \
                                                '-19-170-215.eu-west-1.compute.amazonaws.com:5432/dajoliaojhf3su'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)

    class Player(db.Model):
        __tablename__ = 'player'
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(200), unique=True)
        last_name = db.Column(db.String(200), unique=True)
        password = db.Column(db.String(200), unique=True)
        shirt_number = db.Column(db.String(200), unique=True)
        email = db.Column(db.String(200), unique=True)

        def __init__(self, first_name, last_name, password, shirt_number, email):
            self.first_name = first_name
            self.last_name = last_name
            self.password = password
            self.shirt_number = shirt_number
            self.email = email


    if dev:
        db.create_all()



    app.register_blueprint(views, url_prefix='/')
    return app