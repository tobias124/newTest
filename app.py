from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Dev Mode
dev = False

# init App
app = Flask(__name__)

if dev:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:SuperSecret@localhost/betgame'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://oywafgwhonrxjc' \
                                            ':1fb26b2f767713170d4a21a7a92edcf077c34b0ebdc0f0ac5f2958005bdb35c0@ec2-52' \
                                            '-19-170-215.eu-west-1.compute.amazonaws.com:5432/dajoliaojhf3su'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    tester = db.Column(db.String(200), unique=True)

    def __init__(self, tester):
        self.tester = tester


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = dev
    app.run()
