from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app_login.models import User, db
from . import users_bp
from .forms import EditUserForm
from functools import wraps
from flask import redirect, url_for, flash
from app_login.utils import log_activity

## Permite acesso somente de usuários especificos##
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Faça login para continuar", "warning")
                return redirect(url_for("auth.login"))

            if current_user.role not in roles:
                flash("Você não tem permissão para acessar esta página.", "danger")
                return redirect(url_for("home.index"))
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

#LINK SIDEBAR PARA USER-LIST
@users_bp.route("/")
@login_required
@role_required("admin")
def users_list():
    users = User.query.all()
    return render_template("users/users-list.html", users=users)

#PAGINA DE USER-EDIT
@users_bp.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@role_required("admin")
def users_edit(user_id):

    user = User.query.get_or_404(user_id)
    form = EditUserForm()

    # impedir que o admin remova ou degrade o próprio admin
    if form.validate_on_submit():
        new_role = request.form.get("role")
        new_status = request.form.get("status") 

        old_role = user.role
        old_status = user.status

        if user.id == current_user.id and new_role != "admin":
            flash("Você não pode alterar o próprio nível de administrador.", "danger")
            return redirect(url_for("users.users_edit", user_id=user.id))

        user.role = new_role
        user.status = new_status

        log_activity(current_user,
            f"Alterou usuário ID {user.id} → "
            f"Role: {old_role} → {new_role}, "
            f"Status: {old_status} → {new_status}"
        )
        db.session.commit()


        flash("Nível de acesso atualizado com sucesso!", "success")
        return redirect(url_for("users.users_list"))

    return render_template("users/users-edit.html", user=user, form=form)
