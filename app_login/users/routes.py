from flask import render_template
from flask_login import login_required
from app_login.models import User
from . import users_bp

@users_bp.route("/")
@login_required
def users_list():
    users = User.query.all()
    return render_template("users/users-list.html", users=users)
