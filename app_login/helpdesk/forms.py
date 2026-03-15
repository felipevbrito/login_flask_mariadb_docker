from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class TicketCreateForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired()]
    )
    descricao = TextAreaField(
        "Descrição",
        validators=[DataRequired()]
    )
    submit = SubmitField("Cadastrar o problema")

class TicketReplyForm(FlaskForm):
    mensagem = TextAreaField(
        "Resposta",
        validators=[DataRequired()]
    )
    submit = SubmitField("Enviar")
