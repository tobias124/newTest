from hashlib import sha256
from flask import Blueprint, render_template, request, redirect, url_for, flash
from website import db
from website.models import Player
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import psycopg2



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        player = Player.query.filter_by(email=email).first()
        if player:
            if check_password_hash(player.password, password):
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password, try again', category='error')
    return render_template('login.html')


@auth.route('/sign-up', methods=('POST', 'GET'))
def sign_up():
    players = Player.query
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        shirt_number = request.form.get('shirtNumber')
        player = Player.query.filter_by(email=email).first()
        if player:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
             flash('First must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be longer than 6 characters.', category='error')
        else:
            new_player = Player(email=email, first_name=first_name, last_name=last_name, 
            shirt_number=shirt_number, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_player)
            db.session.commit()
    return render_template('sign-up.html', players = players)
