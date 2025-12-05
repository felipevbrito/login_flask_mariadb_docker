from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from datetime import datetime, timedelta
import uuid

from util import log_event, generate_csrf_token, csrf_protect, limit_login_attempts

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

# Cria as tabelas automaticamente se não existirem
with app.app_context():
    db.create_all()

# antes de cada request
app.before_request(csrf_protect)
app.before_request(limit_login_attempts)

# jinja env
app.jinja_env.globals["csrf_token"] = generate_csrf_token

# Página inicial
@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("pages/index.html", user=session["user"])


@app.route("/home")
def home_redirect():
    return redirect(url_for("index"))

# Cadastro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        # Checar se email ou username já existem
        if User.query.filter((User.email==email)|(User.username==username)).first():
            flash("E-mail ou usuário já cadastrado!", "danger")
            return render_template("register.html")

        user = User(email=email, username=username, password=password, status='active')
        db.session.add(user)
        db.session.commit()
        flash("Usuário criado!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, status='active').first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user"] = user.username
            return redirect(url_for("index"))
        else:
            flash("Login inválido!", "danger")

    return render_template("login.html")

# Forgot
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email, status='active').first()

        if user:
            token = str(uuid.uuid4())
            expires = datetime.utcnow() + timedelta(hours=1)
            user.reset_token = token
            user.token_expires = expires
            db.session.commit()

            reset_link = url_for("reset", token=token, _external=True)
            flash(f"Link de recuperação: {reset_link}", "info")
        else:
            flash("E-mail não encontrado!", "danger")

    return render_template("forgot.html")

# Reset
@app.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    user = User.query.filter_by(reset_token=token, status='active').first()
    if not user:
        flash("Token inválido!", "danger")
        return redirect(url_for("login"))

    if not user.token_expires or user.token_expires < datetime.utcnow():
        flash("Token expirado!", "danger")
        return redirect(url_for("forgot"))

    if request.method == "POST":
        password = generate_password_hash(request.form["password"])
        user.password = password
        user.reset_token = None
        user.token_expires = None
        db.session.commit()
        flash("Senha alterada!", "success")
        return redirect(url_for("login"))

    return render_template("reset.html", token=token)

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

