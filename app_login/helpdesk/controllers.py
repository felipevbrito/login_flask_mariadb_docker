from flask_login import current_user
from app_login.extensions import db
from .models import Ticket, TicketMessage
from flask import request, current_app
from app_login.utils import salvar_imagem_ticket
from .models import TicketImage
from werkzeug.utils import secure_filename
import os

def create_ticket(form):
    ticket = Ticket(
        titulo=form.titulo.data,
        descricao=form.descricao.data,
        usuario_id=current_user.id
    )
    db.session.add(ticket)
    db.session.commit()

    # UPLOAD DE IMAGENS
    #upload_path = os.path.join(current_app.root_path, "uploads", "tickets")
    base_upload = os.path.join(current_app.root_path, "uploads", "tickets")
    ticket_folder = os.path.join(base_upload, str(ticket.id))
    os.makedirs(ticket_folder, exist_ok=True)


    files = request.files.getlist("imagens")
    for file in files:
        if file.filename == "":
            continue
        filename = salvar_imagem_ticket(file, ticket_folder)
        img = TicketImage(ticket_id=ticket.id, filename=filename)
        db.session.add(img)
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

    # UPLOAD DE IMAGENS
    upload_path = os.path.join(current_app.root_path, "uploads", "tickets")
    files = request.files.getlist("imagens")

    for file in files:
        if file.filename == "":
            continue
        filename = salvar_imagem_ticket(file, upload_path)
        img = TicketImage(
            ticket_id=ticket_id,
            filename=filename
        )
        db.session.add(img)
    db.session.commit()