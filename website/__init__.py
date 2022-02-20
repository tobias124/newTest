from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2

# init App
app = Flask(__name__)
dev = False


app.secret_key = "dkslaljköadjlkdasfl1147cx22111###d"
if dev:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:SuperSecret@localhost/betgame'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oywafgwhonrxjc' \
                                            ':1fb26b2f767713170d4a21a7a92edcf077c34b0ebdc0f0ac5f2958005bdb35c0@ec2-52' \
                                            '-19-170-215.eu-west-1.compute.amazonaws.com:5432/dajoliaojhf3su'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# if dev:
#    db.create_all()


def create_app():
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app
