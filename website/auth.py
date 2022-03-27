from hashlib import sha256
from math import remainder
from flask import Blueprint, render_template, request, redirect, url_for, flash
from website import db
from website.models import Player, Game, participates
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
        remember = True #if request.form.get('remember'): True else False implement?
        
        if player:
            if check_password_hash(player.password, password):
                login_user(player, remember=remember)
            else:
                flash('Falsches Passwort, versuche es noch einmal!', category='error')
        else:
            flash('Benutzername ' + username +' existiert nicht!', category='error')
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    return render_template('login.html')

@auth.route('/logout', methods=('POST', 'GET'))
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id):
    player_to_edit = Player.query.get_or_404(id)
    if current_user.role == "ADMIN" or current_user.id == id:
        if request.method == "POST":
            new_username = request.form.get("username")
            other_player = Player.query.filter(Player.username == new_username and Player.id != id).first()
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            
            # if new username != current username
            if new_username != player_to_edit.username:
                if other_player:
                    flash("Benutzername ist leider schon vergeben!", category='error')
                    return render_template('editplayer.html', player_to_edit = player_to_edit)
                elif len(new_username) < 4:
                    flash('Benutzername muss mehr als 3 Zeichen haben.', category='error')
                    return render_template('editplayer.html', player_to_edit = player_to_edit)
            
            if len(password1) != 0 and len(password2) != 0:
                if password1 != password2:
                    flash('Passwords don\'t match.', category='error')
                    return render_template('editplayer.html', player_to_edit = player_to_edit)
                elif len(password1) < 4:
                    flash('Passwort muss länger sein als 3 Zeichen.', category='error')
                    return render_template('editplayer.html', player_to_edit = player_to_edit)
                
            if new_username != player_to_edit.username or (len(password1) != 0 and len(password2) != 0):
                player_to_edit.username = new_username
                player_to_edit.password=generate_password_hash(password1, method='sha256')
                db.session.commit()
                flash('Daten erfolgreich geändert!', category='success')
                
        return render_template('editplayer.html', player_to_edit = player_to_edit)
        
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
            return "Es ist ein Fehler beim Löschen aufgetreten!!"
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
                flash('Benutzername existiert bereits.', category='error')
            elif len(username) < 4:
                flash('Benutzername muss mehr als 3 Zeichen haben.', category='error')
            elif len(first_name) < 2:
                flash('Vorname muss länger sein als 1 Zeichen.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 4:
                flash('Passwort muss länger sein als 3 Zeichen.', category='error')
            else:
                new_player = Player(username=username, first_name=first_name, last_name=last_name, 
                    password=generate_password_hash(password1, method='sha256'), role=role)  

                db.session.add(new_player)
                db.session.commit()
                all_enabled_games = Game.query.filter_by(enabled=True)
                for game in all_enabled_games:
                    statement = participates.insert().values(player_id=new_player.id, game_id=game.id)
                    db.session.execute(statement)
                    db.session.commit()
        return render_template('player.html', current_user = current_user, players = players)
    else:
        return redirect(url_for('views.home'))