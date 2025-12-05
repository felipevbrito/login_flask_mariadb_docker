# 🖥️ Sistema de Login com Flask e MariaDB

## 📁 Estrutura do Projeto
program_login/
│
├── flask_auth/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   │
│   ├── templates/
│   │   ├── pages/
│   │   │   └── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── forgot.html
│   │   ├── reset.html
│   │   └── home.html
│   │
│   └── static/
│       ├── favicon.ico
│       └── style.css
│
├── start.sh
├── docker-compose.yml
├── Dockerfile
└── README.md

## 🗄️ Banco de Dados
- Banco: **MariaDB**  
- Acesso via **SQLAlchemy** (ORM) em `app.py` / `models.py`  
- phpMyAdmin incluso para gerenciamento web do banco

## 🔐 Segurança implementada
- Senhas hashadas com werkzeug.security
- Expiração automática de sessão (configuração de 30 min)
- Proteção CSRF em formulários
- Suporte a HTTPS seguro para cookies (configurável)
- Limitar tentativas de login
- Log de atividades (audit trail)

## ⚡️ Melhorias futuras
- Suporte a múltiplos perfis de usuário / permissões

## 🏃 Como rodar
1. Certifique-se de ter o Docker e Docker Compose instalados.
2. Torne o script `start.sh` executável:
```bash
chmod +x start.sh
```
3. Execute a aplicação:
```bash
./start.sh
```
[Acesse a aplicação](http://localhost:8080)
[Acesse o phpMyAdmin](http://localhost:8081)


