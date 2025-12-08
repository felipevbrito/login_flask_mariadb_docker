from app_login.models import User

def get_all_users():
    return User.query.all()
