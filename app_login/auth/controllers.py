from ..models.auth import User
from ..extensions import db, bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

s = URLSafeTimedSerializer('secret-key')

def create_user(username, email, password):
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed)
    db.session.add(user)
    db.session.commit()
    return user

def verify_password(user, password):
    return bcrypt.check_password_hash(user.password, password)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def confirm_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return email



