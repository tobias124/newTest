from website import db
from website.models import Player
from werkzeug.security import generate_password_hash, check_password_hash

db.create_all()
new_player = Player(email="biasi_eiter@hotmail.com", first_name="Tobias", last_name="Eiter", 
shirt_number=17, password=generate_password_hash("1234", method='sha256'),
role="ADMIN")
db.session.add(new_player)
db.session.commit()