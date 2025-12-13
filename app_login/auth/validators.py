from wtforms.validators import ValidationError
from ..models.auth import User

def validate_email(form, field):
    existing = User.query.filter_by(email=field.data).first()

    # Se estiver alterando email (form tem o id do usuário)
    if existing and hasattr(form, "current_user_id") and existing.id != form.current_user_id:
        raise ValidationError("Este e-mail já está sendo usado por outro usuário.")

    # Caso registro (form não tem current_user_id)
    if existing and not hasattr(form, "current_user_id"):
        raise ValidationError("Este e-mail já está registrado.")
