from flask import request
from app_login.extensions import db
from app_login.models import UserActivityLog

def log_activity(user, action):
    entry = UserActivityLog(
        user_id=user.id,
        action=action,
        ip_address=request.remote_addr,
        user_agent=request.headers.get("User-Agent")
    )
    db.session.add(entry)
    db.session.commit()
