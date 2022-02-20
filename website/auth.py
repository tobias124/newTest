from flask import Blueprint, render_template, request, redirect, url_for, flash
from website import db, Player
from werkzeug.security import generate_password_hash, check_password_hash

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
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        

    return render_template('sign-up.html')
