import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:flaskpass@db:3306/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Chave secreta do Flask
    SECRET_KEY = 'sua_chave_secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_ENABLED = True
