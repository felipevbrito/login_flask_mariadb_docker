from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import helpdesk_bp
from .forms import TicketCreateForm, TicketReplyForm
from .controllers import create_ticket, reply_ticket
from .models import Ticket
from app_login.extensions import db

@helpdesk_bp.route("/tickets")
@login_required
def tickets():
    if current_user.role == "admin":
        tickets = Ticket.query.order_by(
            Ticket.criado_em.desc()
        ).all()
    else:
        tickets = Ticket.query.filter_by(
            usuario_id=current_user.id
        ).order_by(
            Ticket.criado_em.desc()
        ).all()
    return render_template(
        "helpdesk/ticket-list.html",
        tickets=tickets
    )

@helpdesk_bp.route("/tickets/new", methods=["GET", "POST"])
@login_required
def ticket_create():
    if current_user.role == "admin":
        flash("Administradores não podem abrir chamados.", "warning")
        return redirect(url_for("helpdesk.tickets"))
    form = TicketCreateForm()

    if form.validate_on_submit():
        create_ticket(form)
        flash("Chamado criado com sucesso", "success")
        return redirect(url_for("helpdesk.tickets"))
    return render_template(
        "helpdesk/ticket-create.html",
        form=form
    )

@helpdesk_bp.route("/tickets/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def ticket_view(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role != "admin" and ticket.usuario_id != current_user.id:
        flash("Você não tem permissão para acessar este chamado.", "danger")
        return redirect(url_for("helpdesk.tickets"))

    # quando admin abre o ticket → muda para em análise
    if current_user.role == "admin" and ticket.status == "aberto":
        ticket.status = "em_analise"
        db.session.commit()

    form = TicketReplyForm()

    if form.validate_on_submit():
        if ticket.status == "solucionado":
            flash("Este chamado já foi encerrado.", "warning")
            return redirect(url_for("helpdesk.ticket_view", ticket_id=ticket.id))
        reply_ticket(ticket_id, form)

        db.session.commit()
        flash("Resposta enviada", "success")
        return redirect(url_for("helpdesk.ticket_view", ticket_id=ticket_id))

    return render_template(
        "helpdesk/ticket-view.html",
        ticket=ticket,
        form=form
    )

@helpdesk_bp.route("/tickets/<int:ticket_id>/resolve", methods=["POST"])
@login_required
def ticket_resolve(ticket_id):

    if current_user.role != "admin":
        flash("Apenas administradores podem resolver chamados.", "danger")
        return redirect(url_for("helpdesk.tickets"))

    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = "solucionado"
    db.session.commit()
    flash("Chamado marcado como solucionado.", "success")

    return redirect(url_for("helpdesk.ticket_view", ticket_id=ticket_id))