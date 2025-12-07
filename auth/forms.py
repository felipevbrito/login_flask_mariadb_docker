from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Seu email"})
    password = PasswordField('Senha', validators=[DataRequired()], render_kw={"placeholder": "Sua senha"})
    submit = SubmitField('Entrar')
class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar')

class ResetForm(FlaskForm):
    password = PasswordField('Nova senha', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Redefinir')

## Atualizar o user
class ChangeUsernameForm(FlaskForm):
    username = StringField("Novo usuário", validators=[DataRequired(), Length(min=3, max=30)])
    submit_username = SubmitField("Atualizar usuário")
class ChangeEmailForm(FlaskForm):
    email = StringField("Novo e-mail", validators=[DataRequired(), Email()])
    submit_email = SubmitField("Atualizar e-mail")
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Senha atual", validators=[DataRequired()])
    new_password = PasswordField("Nova senha", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar nova senha", validators=[
        DataRequired(),
        EqualTo("new_password", message="As senhas não coincidem.")
    ])
    submit_password = SubmitField("Atualizar senha")
