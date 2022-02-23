from website import db, local_db_link, heroku_db_link, dev
from website.models import *
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2


# conn = psycopg2.connect(
#     database="betgame", user="postgres", password="SuperSecret", host='localhost', port= '5432'
# )

db.create_all()

#Players
new_player = Player(email="biasi_eiter@hotmail.com", first_name="Tobias", last_name="Eiter", 
    password=generate_password_hash("1234", method='sha256'), role="ADMIN")
new_player2 = Player(email="tomturbo@hotmail.com", first_name="Dominik", last_name="Turner", 
     password=generate_password_hash("123456789", method='sha256'),
role="PLAYER")

#Games
new_game = Game(gameday=11, home_team='FC Siglu St. Leonhard',
                                away_team='Spg Raika Pitztal', enabled=True)


db.session.add_all([new_player, new_player2, new_game])
new_player2.paying.append(new_game)

db.session.commit()
##
if dev:
    conn = psycopg2.connect( local_db_link)
else:
    conn = psycopg2.connect(heroku_db_link)

cursor = conn.cursor()

cursor.execute("Select * FROM participates")
data = cursor.fetchall()
print(data)
query = "UPDATE participates SET bet_is_payed = %s WHERE player_id = %s and game_id = %s"
query_data = (True, 9, 15)
cursor.execute(query, query_data)
conn.commit()
cursor.close()
conn.close()

