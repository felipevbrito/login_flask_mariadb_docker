from flask_login import current_user
from app_login.extensions import db
from .models import Ticket, TicketMessage


def create_ticket(form):
    ticket = Ticket(
        titulo=form.titulo.data,
        descricao=form.descricao.data,
        usuario_id=current_user.id
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket


def reply_ticket(ticket_id, form):
    msg = TicketMessage(
        ticket_id=ticket_id,
        usuario_id=current_user.id,
        mensagem=form.mensagem.data
    )
    db.session.add(msg)
    db.session.commit()