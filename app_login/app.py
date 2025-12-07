from flask import Flask, render_template, request
from .config import Config
from .extensions import db
from .models import User
from .extensions import login_manager
from .auth.routes import auth_bp
from .main.routes import main_bp
from flask_wtf.csrf import CSRFProtect
import os

csrf = CSRFProtect()

def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))

    app = Flask(
        __name__,
        static_folder=STATIC_DIR,
        static_url_path='/static'
    )
    app.config.from_object(Config)

    # Inicializa CSRF
    csrf.init_app(app)

    # Inicializa DB
    db.init_app(app)

    # Inicializa Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # BLUEPRINTS
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    # ERROR HANDLERS
    @app.errorhandler(404)
    def not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error/500.html'), 500

    # Criação das tabelas
    with app.app_context():
        db.create_all()

    return app
