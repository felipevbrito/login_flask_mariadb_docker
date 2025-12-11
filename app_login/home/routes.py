from flask import render_template
from . import home_bp
from flask_login import login_required

@home_bp.route('/')
@home_bp.route('/index')
@home_bp.route('/home')

@login_required
def index():
    return render_template('pages/index.html')
