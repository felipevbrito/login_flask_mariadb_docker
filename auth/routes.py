#from flask import render_template, redirect, url_for
#from . import auth_bp

#@auth_bp.get('/login')
#def login():
#    return render_template('authentication/login.html')

from flask import render_template, redirect, url_for, flash, request
from . import auth_bp
from .forms import LoginForm, RegisterForm, ForgotForm, ResetForm
from ..models import User
from ..extensions import db
from flask_login import login_user, logout_user, login_required
from .controllers import create_user, verify_password, generate_reset_token, confirm_reset_token

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and verify_password(user, password):
            login_user(user)
            flash('Logado com sucesso.', 'success')
            next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))
    flash('Usuário ou senha inválida.', 'danger')
    return render_template('authentication/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.email.data, form.password.data)
        flash('Registro criado. Faça login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('authentication/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
    if user:
        token = generate_reset_token(user.email)
        # aqui você enviaria o email com link contendo o token
        flash('Token de recuperação gerado (demo).', 'info')
    else:
        flash('Email não encontrado.', 'warning')
    return render_template('authentication/forgot.html', form=form)

@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    form = ResetForm()
    email = confirm_reset_token(token)
    if not email:
        flash('Token inválido ou expirado.', 'danger')
        return redirect(url_for('auth.forgot'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
    if user:
        from extensions import bcrypt
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash('Senha redefinida. Faça login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('authentication/reset.html', form=form)

