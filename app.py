from flask import Flask, render_template, request
from .config import Config
from .models import db, User
from .extensions import login_manager
from .auth.routes import auth_bp
from .main.routes import main_bp
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
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
    
    import logging
    logging.basicConfig(level=logging.DEBUG)

    @app.before_request
    def log_request():
        logging.debug(f"Rota chamada: {request.path}")

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


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
