from flask import Blueprint

helpdesk_bp = Blueprint(
    "helpdesk",
    __name__,
    url_prefix="/helpdesk"
)

from . import routes

from flask_login import current_user
from .models import Ticket
from . import helpdesk_bp

@helpdesk_bp.app_context_processor
def helpdesk_counter():
    if current_user.is_authenticated and current_user.role == "admin":
        count = Ticket.query.filter(Ticket.status.in_(["aberto", "em_analise"])).count()
        return dict(helpdesk_count=count)

    return dict(helpdesk_count=0)