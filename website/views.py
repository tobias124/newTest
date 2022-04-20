from flask import Blueprint, flash, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from website.models import *
from . import db, dev, local_db_link, heroku_db_link
from website.db_operations import *
import psycopg2
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import delete

views = Blueprint('views', __name__)


def check_Bet_Form_Requirements(home_goals, away_goals):
    return home_goals >= 0 and away_goals >= 0


@views.route('/index')
@login_required
def home():
    games_active = Game.query.filter_by(enabled=True)
    
    db_connection = psycopg2.connect(heroku_db_link)
    cursor = db_connection.cursor()
    query = "SELECT game_id, game.home_team, game.away_team, game.home_goals, game.away_goals\
             FROM bet JOIN game ON game.id = bet.game_id \
             WHERE bet.player_id = %s AND bet.away_goals = game.away_goals AND bet.home_goals = game.home_goals\
             Group by game_id, game.home_team, game.away_team, game.home_goals, game.away_goals\
             Order by game_id desc" % (str(current_user.id),)
    cursor.execute(query)
    games_done = cursor.fetchall()  
    cursor.close()  
    db_connection.close() 
    winners = db.session.query(Bet, Game).filter(Bet.player_id == current_user.id)\
        .join(Game, (Game.id == Bet.game_id)).filter(Bet.away_goals == Game.away_goals, Bet.home_goals == Game.home_goals)
    
    number_of_winners = winners.count()
    number_of_active_games = Game.query.filter_by(enabled=True).count()

    from scrape import glw_table
    from scrape import table_games
 
    return render_template("index.html", user_first_name=current_user.first_name,
                           user_last_name=current_user.last_name, winners=winners, number_of_active_games=number_of_active_games,
                           games_done=games_done, number_of_winners=number_of_winners, games_active=games_active, 
                           glw_table = [glw_table.to_html (header=True, index=False, classes='table-sm table-striped')],
                           table_games = table_games)


@views.route('/bet-delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_bet(id):
    bet_to_delete = Bet.query.get_or_404(id)
    if current_user.id == bet_to_delete.player_id:
        try:
            db.session.delete(bet_to_delete)
            db.session.commit()
            return redirect(url_for('views.bet'))
        except:
            return "Es ist ein Fehler beim Löschen aufgetreten!"
    else:        
        redirect(url_for('views.home'))

@views.route('/bet', methods=['POST', 'GET'])
@login_required
def bet():
    bets = Bet.query.filter_by(player_id=current_user.id)
    games = Game.query.filter_by(enabled=True).filter_by(bet_lock = False)
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
        # set bet is payed to false if new there is a new bet
        # change bet_is_payed boolean of specific game in assoc table
            connection = psycopg2.connect(heroku_db_link)
            cursor = connection.cursor()
            query = "UPDATE participates SET bet_is_payed = %s WHERE player_id = %s and game_id = %s"
            query_data = (False, player_id, game_id)
            cursor.execute(query, query_data)
            connection.commit()
            cursor.close()
            connection.close()
        else:
            flash("Negative Anzahl Tore nicht möglich", category='error')
    return render_template("bet.html", name=current_user.first_name, bets=bets, active_games=games)

@views.route('/lockbet/<int:id>')
@login_required
def lockbet(id):
    if current_user.role == "ADMIN":
        game_to_change_lock = Game.query.get_or_404(id)
        if not game_to_change_lock.bet_lock:
            game_to_change_lock.bet_lock = True
            flash("Für " + game_to_change_lock.home_team + " vs. " + game_to_change_lock.away_team + " können keine Tipps mehr abgegeben werden!", category='success')
        else:
            game_to_change_lock.bet_lock = False
            flash("Tippen für das Spiel: " + game_to_change_lock.home_team + " vs. " + game_to_change_lock.away_team + " erfolgreich freigegeben.", category='success')
        try:
            db.session.commit()
            return redirect(url_for('views.games'))
        except:
            return "There was a problem changing bet status!"
    else:
        return redirect(url_for('views.home'))

@views.route('/games', methods=['POST', 'GET'])
@login_required
def games():
    if current_user.role == "ADMIN":
        all_players = Player.query
        games = Game.query.filter_by().order_by(Game.gameday.asc())
        winners = db.session.query(Bet, Game, Player).filter()\
            .join(Game, (Game.id == Bet.game_id))\
            .join(Player, (Bet.player_id == Player.id))\
            .filter(Bet.away_goals == Game.away_goals, Bet.home_goals == Game.home_goals)
        games_done = Game.query.filter_by(enabled=False).order_by(Game.gameday.desc())
        if request.method == 'POST':
            # Add new game:
            if request.form.get('add_game_const') == '1':
                gameday = request.form.get('gameday')
                if(gameday.isnumeric()):
                    home_team = request.form.get('home_team')
                    away_team = request.form.get('away_team')
                    new_game = Game(gameday=gameday, home_team=home_team,
                                    away_team=away_team, enabled=True)
                    db.session.add(new_game)

                    # all player and new game in assoc table
                    for player in all_players:
                        player.paying.append(new_game)

                    db.session.commit()

                    connection = psycopg2.connect(heroku_db_link)

                    # change bet_is_payed boolean of specific game in assoc table
                    cursor = connection.cursor()
                    for player in all_players:
                        query = "UPDATE participates SET bet_is_payed = %s WHERE player_id = %s and game_id = %s"
                        query_data = (False, player.id, new_game.id)
                        cursor.execute(query, query_data)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    flash("Game added successfully!", category='success')
                else:
                    flash("Nur positive Zahl für Spieltag möglich!", category='error')
            # Edit Game Data:
            elif request.form.get('edit_game_const') == '1' and (request.form.get('home_goals_result') != "" and request.form.get('away_goals_result') != ""):
                if request.form.get('home_goals_result').isnumeric() and request.form.get('away_goals_result').isnumeric():
                    home_goals_result = int(request.form.get('home_goals_result'))
                    away_goals_result = int(request.form.get('away_goals_result'))
                    current_game = int(request.form.get('current_game'))
                    game_to_update = Game.query.get(current_game)
                    game_to_update.home_goals = home_goals_result
                    game_to_update.away_goals = away_goals_result
                    game_to_update.enabled = False
                    game_to_update.bet_lock = True
                    # save winner ??
                    db.session.commit()
                    flash("Game updated successfully!", category='success')
                else:
                    flash("Nur positive Zahleingaben möglich", category="error")
            # Delete Game
            elif request.form.get('delete') == '1':
                current_game = int(request.form.get('current_game'))
                bets_to_delete = Bet.query.filter_by(game_id=current_game)
                game_to_delete = Game.query.get(current_game)
                # Delete Bets
                for bets in bets_to_delete:
                    db.session.delete(bets)
                    db.session.commit()
                # Delete entries in pariticpates
                db_connection = psycopg2.connect(heroku_db_link)
                cursor = db_connection.cursor()
                query = "DELETE FROM participates WHERE game_id = %s"%(str(current_game))
                cursor.execute(query)
                db_connection.commit()
                cursor.close()
                db_connection.close()
                db.session.delete(game_to_delete)
                db.session.commit()

                flash("Game deleted successfully!", category='success')
        from scrape import table_games
        return render_template('games.html', table_games = table_games, active_games=games, winners=winners, games_done=games_done)
    else:
        return redirect(url_for('views.home'))

@views.route("/pay", methods=['POST', 'GET'])
@login_required
def payment():
    if current_user.role == "ADMIN":
        player_amount = Player.query.count()
        # games and payment_information both are ordered desc for output (game one time then corresp. table)
        games = Game.query.order_by(Game.id.desc())
        game_amount = games.count()
        db_connection = psycopg2.connect(heroku_db_link)
        cursor = db_connection.cursor()
        #payment table - payment information
        # 0 Betrag, 1 home_team, 2 away team, 3 bet_is_payed, 4 player_first_name, 5 player_last_name, 6 game_id, 7 pl.id
        cursor.execute("\
        Select *\
        FROM\
        (\
            Select CASE WHEN Count(g.id) < 5 THEN 5 ELSE COUNT(g.id) END as betrag, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, g.id as game_id,\
                pl.id\
            FROM participates as p join Player as pl on p.player_id = pl.id join Game as g on g.id = p.game_id\
                join bet as b on b.player_id = pl.id and b.game_id = g.id\
            GROUP BY g.id, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, pl.id\
                \
            UNION ALL\
                \
            Select CASE WHEN Count(g.id) < 5 THEN 5 ELSE COUNT(g.id) END as Betrag, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, g.id as game_id,\
                pl.id\
            FROM participates as p join Player as pl on p.player_id = pl.id join Game as g on g.id = p.game_id left join bet\
                on pl.id = bet.player_id and g.id = bet.game_id\
            Where bet.id is NULL\
            GROUP BY g.id, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, pl.id\
        ) as x\
            ORDER BY x.game_id desc\
        ")
        payment_information = cursor.fetchall()
         
        #total betrag for each game 
        cursor.execute("\
        Select x.game_id, CAST(sum(betrag) as INTEGER) as total\
        FROM\
        (\
            Select CASE WHEN Count(g.id) < 5 THEN 5 ELSE COUNT(g.id) END as betrag, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, g.id as game_id,\
                pl.id\
            FROM participates as p join Player as pl on p.player_id = pl.id join Game as g on g.id = p.game_id\
                join bet as b on b.player_id = pl.id and b.game_id = g.id\
            GROUP BY g.id, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, pl.id\
                \
            UNION ALL\
                \
            Select CASE WHEN Count(g.id) < 5 THEN 5 ELSE COUNT(g.id) END as Betrag, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, g.id as game_id,\
                pl.id\
            FROM participates as p join Player as pl on p.player_id = pl.id join Game as g on g.id = p.game_id left join bet\
                on pl.id = bet.player_id and g.id = bet.game_id\
            Where bet.id is NULL\
            GROUP BY g.id, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, pl.id\
        ) as x\
		Group BY x.game_id, betrag\
        ORDER BY x.game_id desc")
        
        # total_payment [(game_id, total), (game_id, total)] acess with totalpayment[x][y]
        total_payment = cursor.fetchall()
        
        #payed
        cursor.execute("Select game_id, Sum(betrag)\
        FROM\
        (\
            Select CASE WHEN Count(g.id) < 5 THEN 5 ELSE COUNT(g.id) END as betrag, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, g.id as game_id,\
                pl.id\
            FROM participates as p join Player as pl on p.player_id = pl.id join Game as g on g.id = p.game_id\
                join bet as b on b.player_id = pl.id and b.game_id = g.id\
            GROUP BY g.id, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, pl.id\
			            UNION ALL\
                \
            Select CASE WHEN Count(g.id) < 5 THEN 5 ELSE COUNT(g.id) END as Betrag, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, g.id as game_id,\
                pl.id\
            FROM participates as p join Player as pl on p.player_id = pl.id join Game as g on g.id = p.game_id left join bet\
                on pl.id = bet.player_id and g.id = bet.game_id\
            Where bet.id is NULL\
            GROUP BY g.id, g.home_team, g.away_team, p.bet_is_payed, pl.first_name, pl.last_name, pl.id\
        ) as x\
		WHERE x.bet_is_payed = 'True'\
		GROUP BY game_id\
		ORDER BY x.game_id desc\
")

        payed_sum = cursor.fetchall()

        #games_not_payed - List  
        cursor.execute("Select g.id as game_id\
        FROM game as g join participates as p on g.id = p.game_id\
        group by g.id, p.bet_is_payed\
        having bet_is_payed = false")
        
        games_not_payed = [list(i) for i in cursor.fetchall()]
        games_not_payed = [item for sublist in games_not_payed for item in sublist]
        cursor.close()
        db_connection.close()
        if request.method == 'POST': 
            # game id | Player id - iterate amoutn of game | player 
            data_pay_form = request.form.getlist('payment_checkbox')     
    
            if(data_pay_form):
                # Set up DB connection
                db_connection = connect_psycopg2(heroku_db_link)
                cursor = db_connection.cursor()
                query ="UPDATE participates SET bet_is_payed = true WHERE game_id = %s AND player_id = %s"
                # update all
                for data in data_pay_form:  
                    data = data.split(",")   
                    query_data = (data[0], data[1])
                    cursor.execute(query, query_data)
                db_connection.commit()
                #Close DB Conn after execution
                cursor.close()
                db_connection.close()
            flash("Changed successfully!", category='success')
            return redirect(url_for('views.payment'))
        return render_template("pay.html", payment_information=payment_information, 
            games_not_payed = games_not_payed, games=games, player_amount=player_amount,
            total_payment = total_payment, payed_sum = payed_sum)
    return redirect(url_for('views.home'))

@views.route('/bet-details')
@login_required
def bet_details():
    if current_user.role == "ADMIN":
        games = Game.query
        statistics = db.session.query(Bet, Player).filter(Bet.player_id == Player.id).all()
        db_connection = psycopg2.connect(heroku_db_link)
        # cursor = db_connection.cursor()
        # cursor.execute("Select bet.game_id, player.id, player.first_name, player.last_name, bet.participant, home_goals, away_goals\
        #                 FROM bet join player on bet.player_id = player.id\
        #                 ORDER BY game_id, player.id asc")
        # test = cursor.fetchall()
        # cursor.close()
        # db_connection.close()
        return render_template("bet-details.html", games = games, statistics = statistics)
    return redirect(url_for('views.home'))