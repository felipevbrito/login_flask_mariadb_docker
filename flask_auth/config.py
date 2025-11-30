from datetime import timedelta

# Configuração do MariaDB
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:flaskpass@db:3306/flaskdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Chave secreta do Flask
SECRET_KEY = 'sua_chave_secreta'

# Sessão permanente e cookies
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # tempo de expiração da sessão
SESSION_COOKIE_HTTPONLY = True                      # impede acesso via JS
SESSION_COOKIE_SECURE = False                       # colocar True em produção com HTTPS
