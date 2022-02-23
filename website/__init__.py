import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2

# init App
app = Flask(__name__)
dev = False

#Local_DB_Connection
local_db_link = 'postgresql://postgres:SuperSecret@localhost/betgame'
# Herouku DB Connection 
heroku_db_link = os.environ['DATABASE_URL']


app.secret_key = "dkslaljköadjlkdasfl1147cx22111###d"
if dev:
    app.config['SQLALCHEMY_DATABASE_URI'] = local_db_link
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = heroku_db_link
    #psycopg2.connect(heroku_db_link)
    

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
