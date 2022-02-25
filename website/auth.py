from hashlib import sha256
from math import remainder
from flask import Blueprint, render_template, request, redirect, url_for, flash
from website import db
from website.models import Player
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import psycopg2



auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        player = Player.query.filter_by(username=username).first()
        remember = True if request.form.get('remember') else False #implement?
        
        if player:
            if check_password_hash(player.password, password):
                login_user(player, remember=remember)
            else:
                flash('Falsches Password, versuche es noch einmal!', category='error')
        else:
            flash('Benutzername ' + username +' existiert nicht!', category='error')
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    return render_template('login.html')

@auth.route('/logout', methods=('POST', 'GET'))
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.role == "ADMIN":
        player_to_delete = Player.query.get_or_404(id)
        try:
            db.session.delete(player_to_delete)
            db.session.commit()
            return redirect(url_for('auth.player'))
        except:
            return "There was a problem deleteting that Player!"
    else:
        return redirect(url_for('views.home'))

@auth.route('/player', methods=['POST', 'GET'])
@login_required
def player():
    if current_user.role == "ADMIN":
        players = Player.query
        if request.method == 'POST':
            username = request.form.get('username')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            role = "PLAYER"
            player = Player.query.filter_by(username=username).first()
            if player:
                flash('username already exists.', category='error')
            elif len(username) < 4:
                flash('username must be greater than 3 characters.', category='error')
            elif len(first_name) < 2:
                flash('First must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 4:
                flash('Password must be longer than 3 characters.', category='error')
            else:
                new_player = Player(username=username, first_name=first_name, last_name=last_name, 
                    password=generate_password_hash(password1, method='sha256'), role=role)
                db.session.add(new_player)
                db.session.commit()
        return render_template('player.html', current_user = current_user, players = players)
    else:
        return redirect(url_for('views.home'))