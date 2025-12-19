import os
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_login import current_user, logout_user
from app_login.config import Config
from app_login.extensions import db, csrf, login_manager
from app_login.utils import log_activity
from app_login.models.auth import User
from app_login.auth.routes import auth_bp
from app_login.home.routes import home_bp
from app_login.users import users_bp
from datetime import timedelta

def create_app():
    # Caminhos externos do /template e /static
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'templates'))
    STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))

    # Criação do app com static fora do pacote
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR, static_url_path='/static')
    app.config.from_object(Config)
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=20)

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

    #Token de validacao da seção
    @app.before_request
    def check_single_session():
        if current_user.is_authenticated:
            token_db = current_user.session_token
            token_session = session.get('session_token')

            if token_db != token_session:
                logout_user()
                session.pop('session_token', None)

                flash(
                    "Sessão encerrada: você fez login em outro dispositivo.",
                    "warning"
                )
                return redirect(url_for("auth.login"))

    # Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(home_bp)
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

    from flask_wtf.csrf import generate_csrf

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf())

    # Garante criação das tabelas (somente dev)
    with app.app_context():
        db.create_all()

    return app



