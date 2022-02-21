from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from website.models import Bet, Game
from . import db

views = Blueprint('views', __name__)


def check_Bet_Form_Requirements(home_goals, away_goals):
    return home_goals >= 0 and away_goals >= 0


@views.route('/index')
@login_required
def home():
    return render_template("index.html", user_first_name=current_user.first_name,
                           user_last_name=current_user.last_name)


@views.route('/bet', methods=['POST', 'GET'])
@login_required
def bet():
    bets = Bet.query.filter_by(player_id=current_user.id)
    games = Game.query.filter_by(enabled=True)
    if request.method == 'POST':
        participant = request.form.get('participant')
        home_goals = int(request.form.get('home_goals'))
        away_goals = int(request.form.get('away_goals'))
        player_id = current_user.id
        game_id = int(request.form.get('game_id'))
        if check_Bet_Form_Requirements(home_goals, away_goals):
            new_bet = Bet(participant=participant, home_goals=home_goals, away_goals=away_goals,
                          player_id=player_id, game_id=game_id)
            db.session.add(new_bet)
            db.session.commit()
        else:
            flash("Negative Anzahl Tore nicht möglich", category='error')
    return render_template("bet.html", name=current_user.first_name, bets=bets, active_games=games)


@views.route('games', methods=['POST', 'GET'])
def games():
    games = Game.query.filter_by()#enabled=True)
    if request.method == 'POST':
        # Add new game:
        if request.form.get('add_game_const') == '1':
            gameday = request.form.get('gameday')
            home_team = request.form.get('home_team')
            away_team = request.form.get('away_team')
            new_game = Game(gameday=gameday, home_team=home_team,
                            away_team=away_team, enabled=True)
            db.session.add(new_game)
            db.session.commit()
        # Edit Game Data:
        elif request.form.get('edit_game_const') == '1' and (request.form.get('home_goals_result') != "" and request.form.get('away_goals_result') != ""):
            if int(request.form.get('home_goals_result')) >= 0 and int(request.form.get('away_goals_result')) >= 0:
                home_goals_result = int(request.form.get('home_goals_result'))
                away_goals_result = int(request.form.get('away_goals_result'))
                current_game = int(request.form.get('current_game'))
                game_to_update = Game.query.get(current_game)
                game_to_update.home_goals = home_goals_result
                game_to_update.away_goals = away_goals_result
                game_to_update.enabled = False
                db.session.commit()
                flash("Game updated successfully!", category='success')
        # Delete Game
        elif request.form.get('delete') == '1':
            current_game = int(request.form.get('current_game'))
            bets_to_delete = Bet.query.filter_by(game_id = current_game)
            game_to_delete = Game.query.get(current_game)
            for bets in bets_to_delete:
                db.session.delete(bets)
            db.session.delete(game_to_delete)
            db.session.commit()
            
            flash("Game deleted successfully!", category='success')
    return render_template('games.html', active_games=games)
