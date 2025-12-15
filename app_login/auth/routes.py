from flask import render_template, redirect, url_for, flash, request, session
from . import auth_bp
from .forms import LoginForm, RegisterForm, ForgotForm, ResetForm, ChangeUsernameForm, ChangeEmailForm, ChangePasswordForm
from ..models.auth import User
from ..extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import bcrypt
from .controllers import create_user, verify_password, generate_reset_token, confirm_reset_token
from datetime import datetime
import secrets

#------ CRUD BASICO -----#
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        
        if user and verify_password(user, password):
            user.last_access = datetime.utcnow()
            token = secrets.token_hex(32) #gera token session
            user.session_token = token  
            db.session.commit()
            login_user(user)
            session.permanent = True      #para deslogar depois de um tempo
            session['session_token'] = user.session_token
            flash('Bem-vindo ao sistema!', 'success')
            return redirect(url_for('home.index'))
        flash('Email ou senha inválidos.', 'danger')

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
    current_user.last_access = datetime.utcnow()
    db.session.commit()
    logout_user()
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    token = None

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_reset_token(user.email)
            reset_link = url_for('auth.reset', token=token, _external=True)
            flash('Token de recuperação gerado (demo).', 'info')
        else:
            flash('Email não encontrado.', 'warning')

    return render_template('authentication/forgot.html', form=form, token=token)

@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    form = ResetForm()
    email = confirm_reset_token(token)

    if not email:
        flash('Token inválido ou expirado.', 'danger')
        return redirect(url_for('auth.forgot'))
    
    user = User.query.filter_by(email=email).first_or_404()
    
    if form.validate_on_submit():
        if user:
            from ..extensions import bcrypt
            user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            flash('Senha redefinida. Faça login.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('authentication/reset.html', form=form)

#Para o profile
@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('pages/profile.html')

#para alterar USER
@auth_bp.route('/pages/username', methods=['GET', 'POST'])
@login_required
def profile_username():
    form = ChangeUsernameForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("home.index"))

    return render_template('pages/profile-name.html', form=form)

#para alterar Email
@auth_bp.route('/profile/email', methods=['GET', 'POST'])
@login_required
def profile_email():
    form = ChangeEmailForm()
    form.current_user_id = current_user.id  

    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash("E-mail atualizado com sucesso!", "success")
        return redirect(url_for("home.index"))

    return render_template('pages/profile-email.html', form=form)

#para alterar Senha
@auth_bp.route('/profile/password', methods=['GET', 'POST'])
@login_required
def profile_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():        
        if not bcrypt.check_password_hash(current_user.password, form.current_password.data):
            flash("Senha atual incorreta.", "danger")
            return redirect(url_for("auth.profile-password"))

        current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        db.session.commit()

        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for("home.index"))

    return render_template('pages/profile-password.html', form=form)
