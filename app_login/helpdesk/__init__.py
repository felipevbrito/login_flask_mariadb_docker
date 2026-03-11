from flask import Blueprint

helpdesk_bp = Blueprint(
    "helpdesk",
    __name__,
    url_prefix="/helpdesk"
)

from . import routes