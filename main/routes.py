from flask import render_template
from . import main_bp
from flask_login import login_required, current_user

@main_bp.route('/')
@main_bp.route('/index')
@main_bp.route('/home')

@login_required
def index():
    print("AUTH:", current_user.is_authenticated)
    return render_template('pages/index.html')
