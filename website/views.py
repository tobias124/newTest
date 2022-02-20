from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("index.html", user_first_name = current_user.first_name, 
    user_last_name = current_user.last_name)

@views.route('/bet')
@login_required
def bet():
    return render_template("bet.html", name=current_user.first_name)