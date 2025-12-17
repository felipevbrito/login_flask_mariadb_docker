from ..extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user") # opções: "admin", "gestor", "user"
    last_access = db.Column(db.DateTime, nullable=True)
    reset_token = db.Column(db.String(255), nullable=True)
    token_expires = db.Column(db.DateTime, nullable=True)
    session_token = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active') # valores: active / inactive / deleted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

class UserActivityLog(db.Model):
    __tablename__ = "user_activity_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
