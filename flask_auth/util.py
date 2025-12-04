import logging
import secrets
from flask import session, request, abort, flash, redirect, url_for
from datetime import datetime, timedelta

#configuração de logs
logging.basicConfig(
    filename='activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_event(event, user=None, ip=None):
    msg = f"{event} - user: {user}, ip: {ip}"
    logging.info(msg)


# Antes de cada request, sistema de proteção CSRF
def csrf_protect():
    if request.method == "POST":
        token = session.get("_csrf_token")
        if not token or token != request.form.get("_csrf_token"):
            abort(400, description="CSRF token missing or incorrect")

def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(16)
    return session["_csrf_token"]

#limite de tentativas
MAX_ATTEMPTS = 25
LOCKOUT_TIME = timedelta(minutes=15)

def limit_login_attempts():
    # Ignorar GET (obrigatório)
    if request.method == "GET":
        return None

def limit_login_attempts2():
    if request.endpoint == 'login' and request.method == 'POST':
        attempts = session.get("login_attempts", 0)
        last_attempt = session.get("last_attempt")
        now = datetime.utcnow()

        if last_attempt and attempts >= MAX_ATTEMPTS:
            last_attempt_dt = datetime.strptime(last_attempt, "%Y-%m-%d %H:%M:%S")
            if now - last_attempt_dt < LOCKOUT_TIME:
                flash("Muitas tentativas. Tente novamente mais tarde.", "danger")
                return redirect(url_for("login"))
            else:
                session["login_attempts"] = 0

        session["login_attempts"] = attempts + 1
        session["last_attempt"] = now.strftime("%Y-%m-%d %H:%M:%S")

