# app.py
from flask import Flask
app = Flask(__name__)

from model import *
@app.teardown_appcontext
def shutdown_session(exception=None):  # exception=None is needed
    db_session.remove()


@app.route('/')
def hello_world():
    q = User.query.filter(User.username == 'guest').first()
    return 'Hello, {}! Your username is {} and password is {}'.format(q.name, q.username, q.password)


if __name__ == '__main__':
    app.run()