from flask import render_template
from . import main_bp
from flask_login import login_required

@main_bp.route('/')
@main_bp.route('/index')
@main_bp.route('/home')

@login_required
def index():
    return render_template('pages/index.html')
