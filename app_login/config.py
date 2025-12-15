import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:flaskpass@db:3306/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Chave secreta do Flask
    SECRET_KEY = 'sua_chave_secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_ENABLED = True

    #para envio de email e recuparecao de senha
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'seu_email@gmail.com'
    MAIL_PASSWORD = 'senha_de_app'
    MAIL_DEFAULT_SENDER = 'Seu Sistema <seu_email@gmail.com>'
