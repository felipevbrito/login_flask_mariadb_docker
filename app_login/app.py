import os
from flask import Flask, request, render_template
from flask_login import current_user
from app_login.config import Config
from app_login.extensions import db, csrf, login_manager
from app_login.utils import log_activity
from app_login.models import User
from app_login.auth.routes import auth_bp
from app_login.main.routes import main_bp
from app_login.users import users_bp



def create_app():
    # Caminho do /static externo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))

    # Criação do app com static fora do pacote
    app = Flask(
        __name__,
        static_folder=STATIC_DIR,
        static_url_path='/static'
    )
    app.config.from_object(Config)

    # Extensões
    csrf.init_app(app)
    db.init_app(app)

    # Rastrear acesso às páginas
    @app.before_request
    def track_page_access():
        if current_user.is_authenticated:
            path = request.path

            # Ignora arquivos estáticos
            if not path.startswith("/static"):
                log_activity(current_user, f"Acessou a página {path}")

    # Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)

    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error/404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error/403.html"), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error/500.html"), 500

    # Garante criação das tabelas (somente dev)
    with app.app_context():
        db.create_all()

    return app
