from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app_login.models.auth import User, UserActivityLog, db
from . import users_bp
from .forms import EditUserForm
from functools import wraps
from flask import redirect, url_for, flash
from app_login.utils import log_activity, parse_browser, paginate
from app_login.auth.controllers import generate_reset_token


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
@users_bp.route("/admin")
@login_required
@role_required("admin")
def users_list():
    page = request.args.get("page", 1, type=int)

    query_user = ( db.select(User).where(User.status.in_(["active", "inactive"])).order_by(User.id.asc()))
    pagination = paginate(query_user, page=page, per_page=10)

    return render_template("users/users-list.html",users=pagination.items, pagination=pagination)

#LINK SIDEBAR PARA USER-GESTOR
@users_bp.route("/gestor")
@login_required
@role_required("gestor")
def users_gestor():
    users = User.query.all()
    return render_template("users/users-gestor.html", users=users)

#LINK SIDEBAR PARA USER
@users_bp.route("/usuario")
@login_required
def users():
    users = User.query.all()
    return render_template("users/users.html", users=users)

# PÁGINA DE USER-VIEW (ADMIN)
@users_bp.route("/users/view/<int:user_id>", methods=["GET"])
@login_required
@role_required("admin")
def users_view(user_id):

    # Usuário visualizado
    user = User.query.get_or_404(user_id)

    # Últimas 5 atividades do usuário
    activities = (
        UserActivityLog.query
        .filter_by(user_id=user.id)
        .order_by(UserActivityLog.timestamp.desc())
        .limit(5)
        .all()
    )

    # Log da ação administrativa
    for log in activities:
        log.browser = parse_browser(log.user_agent)
        

    log_activity(
        current_user,
        f"Visualizou detalhes do usuário ({user.username})"
    )
    db.session.commit()

    return render_template(
        "users/users-view.html",
        user=user,
        activities=activities
    )

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

# FALSE DELETE DE USER 
@users_bp.route("/delete/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def users_delete(user_id):

    user = User.query.get_or_404(user_id)
    # Impede autoexclusão
    if user.id == current_user.id:
        flash("Você não pode excluir sua própria conta.", "danger")
        return redirect(url_for("users.users_view", user_id=user.id))
    
    user.status = "deleted"
    db.session.commit()

    flash("Usuário excluído com sucesso.", "success")
    return redirect(url_for("users.users_list"))



#reset de senha pelo admin
@users_bp.route("/users/reset-password/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def users_reset_password(user_id):
    user = User.query.get_or_404(user_id)
    token = generate_reset_token(user.email)
    reset_link = url_for('auth.reset', token=token, _external=True)
    
    # Em ambiente local, apenas mostra o link em flash
    flash(f"Link de redefinição de senha (demo): <a href='{reset_link}'>{reset_link}</a>", "info")
    
    # Em produção, aqui você enviaria o email:
    # send_email(user.email, "Redefinição de senha", reset_link)

    return redirect(url_for("users.users_view", user_id=user.id))

