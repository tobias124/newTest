from venv import create
from website import db, local_db_link, heroku_db_link, dev
from website.models import *
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2


#### PLAYER

# Philipp Eckhart
# Günther Eiter
# Tobias Eiter
# Fabian Flir
# Stefan Gabl
# Patrick Gastl
# Utku Girgin
# Jeremias Haueis
# Simon Horn
# Gregor Jäger
# Jürgen Köll
# Simon Lentsch
# Manuel Mark
# Birol Neseli
# Florian Pertl
# Daniel Santeler
# Markus Scholz
# Phillip Schöpf
# Dominik Stoll
# Simon Stoll
# Dominik Thurner
# Mathias Thöni
# Marco Thünauer
# Mathias Walch
# Phillip Wechselberger

db.create_all()

new_player = Player(username="TobiasEiter", first_name="Tobias", last_name="Eiter", 
    password=generate_password_hash("1234", method='sha256'), role="ADMIN")

new_player2 = Player(username="DominikThurner", first_name="Dominik", last_name="Turner", 
     password=generate_password_hash("123456789", method='sha256'), role="PLAYER")

#Games
new_game = Game(gameday=1, home_team='Spg Pitzal',
                                away_team='Umhausen', enabled=True)


db.session.add_all([new_player, new_player2, new_game])
new_player.paying.append(new_game)
new_player2.paying.append(new_game)

db.session.commit()

conn = psycopg2.connect(heroku_db_link) # local or heroku (is set in init)

cursor = conn.cursor()

cursor.execute("Select * FROM participates")
data = cursor.fetchall()
print(data)
query = "UPDATE participates SET bet_is_payed = %s WHERE player_id = %s and game_id = %s"
query_data = (False, 1, 1)
cursor.execute(query, query_data)
query = "UPDATE participates SET bet_is_payed = %s WHERE player_id = %s and game_id = %s"
query_data = (False, 2, 1)
cursor.execute(query, query_data)
conn.commit()
cursor.close()
conn.close()

