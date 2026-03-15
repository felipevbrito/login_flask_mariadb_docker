from app_login.extensions import db
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="aberto")
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    mensagens = db.relationship("TicketMessage", backref="ticket", lazy=True)
    images = db.relationship("TicketImage",backref="ticket",lazy=True,cascade="all, delete-orphan")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
class TicketMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("tickets.id"))
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    usuario = db.relationship("User")
    mensagem = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class TicketImage(db.Model):
    __tablename__ = "ticket_images"

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("tickets.id"),nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime,default=datetime.utcnow)