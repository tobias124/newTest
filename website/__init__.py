import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2

# init App
app = Flask(__name__)

# Deploying on heroku dev = FALSE and use_heroku_db_localy = False
dev = False  
use_heroku_db_locally = False

local_db_link = 'postgresql://postgres:SuperSecret@localhost/betgame'

######## DB HEROKU LOCALLY OR NOT ##########

if dev and use_heroku_db_locally:
    # Heroku Local
    heroku_db_link = 'postgresql://oywafgwhonrxjc:1fb26b2f767713170d4a21a7a92edcf077c34b0ebdc0f0ac5f2958005bdb35c0@ec2-52-19-170-215.eu-west-1.compute.amazonaws.com:5432/dajoliaojhf3su'
elif not dev and not use_heroku_db_locally:
    ## WHEN RUNNING ON HEROKU (IF DATABASE URL CHANGES) 
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL != None:
        heroku_db_link = DATABASE_URL.replace("postgres", "postgresql")
else: #local with local db
    heroku_db_link = local_db_link

############################################

app.secret_key = "dkslaljköadjlkdasfl1147cx22111###d"


app.config['SQLALCHEMY_DATABASE_URI'] = heroku_db_link


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .models import Player

if dev:
    db.create_all()


def create_app():
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(player_id):
         # since the user_id is just the primary key of our user table, use it in the query for the user
        return Player.query.get(int(player_id))

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app
