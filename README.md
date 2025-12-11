# 🖥️ Sistema de Login com Flask e MariaDB

## 📁 Estrutura do Projeto
program_login/
│
├── run.py
│
├── app_login/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── utils.py
│   │
│   ├── auth/
│   │     ├── __init__.py
│   │     ├── controllers.py
│   │     ├── forms.py
│   │     ├── routes.py
│   │     └── validators.py 
│   │
│   ├── users/
│   │     ├── __init__.py
│   │     ├── controllers.py
│   │     ├── forms.py
│   │     └── routes.py 
│   │
│   ├── home/
│   │     ├── __init__.py
│   │     └── routes.py
│   │
│   └── templates/
│           ├── authentication/
│           │       ├── forgot.html
│           │       ├── login.html
│           │       ├── logout.html
│           │       ├── register.html
│           │       └── reset.html
│           │
│           ├── error/
│           │       ├── 403.html
│           │       ├── 404.html
│           │       └── 500.html
│           │
│           ├── includes/
│           │       ├── footer.html
│           │       ├── head.html
│           │       ├── navigation.html
│           │       ├── sidebar.html
│           │       └── modals/
│           │                ├── modalContato.html
│           │                ├── modalPrivacidade.html
│           │                └── modalTermos.html
│           │
│           ├── layouts/
│           │         ├── base-auth.html
│           │         └── base.html
│           │
│           │
│           ├── pages/
│           │       ├── index.html
│           │       ├── profile-email.html
│           │       ├── profile-name.html
│           │       ├── profile-password.html
│           │       └── profile.html
│           │
│           └── users/
│                   ├── users-edit.html
│                   ├── users-list.html
│                   └── users-view.html
│
├── static/
│   ├── css/
│   │     ├── custom.css
│   │     └── forms.css
│   ├── images/
│   │     └── avatar.png
│   ├── js/
│   │     ├── index.js
│   │     └── bootstrap.bundle.min.js
│   └── icons/
│         └── favicon.ico
│
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .gitignore
├── start.sh
└── README.md


## 🗄️ Banco de Dados
- Banco: **MariaDB**  
- Acesso via **SQLAlchemy** (ORM) em `app.py` / `models.py`  
- phpMyAdmin incluso para gerenciamento web do banco

## 🔐 Segurança implementada
- Senhas hashadas com BYCRYPT
- Expiração automática de sessão (configuração de 30 min)
- Proteção CSRF em formulários
- Suporte a HTTPS seguro para cookies (configurável)
- Limitar tentativas de login
- Log de atividades (direto no banco)

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


