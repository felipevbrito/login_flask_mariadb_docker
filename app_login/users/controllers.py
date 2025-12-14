from program_login.app_login.models.auth import User

def get_all_users():
    return User.query.all()
