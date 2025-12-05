from flask import render_template
from . import main_bp
from flask_login import login_required, current_user

@main_bp.route('/')
def index():
    return render_template('pages/index.html')
