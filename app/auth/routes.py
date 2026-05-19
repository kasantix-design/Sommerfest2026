from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth.forms import ForgotPasswordForm, LoginForm, ResetPasswordForm
from app.extensions import db
from app.models import AdminInvite, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/logg-inn", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("main.my_registration"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()

        if not user or not user.check_password(form.password.data):
            flash("Feil e-post eller passord.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user, remember=True)

        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)

        if user.is_admin:
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("main.my_registration"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logg-ut")
@login_required
def logout():
    logout_user()
    flash("Du er logget ut.", "success")
    return redirect(url_for("main.index"))


@auth_bp.route("/glemt-passord", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        flash(
            "Hvis e-posten finnes, blir en tilbakestillingslenke sendt.",
            "info",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html", form=form)


@auth_bp.route("/ny-admin/<token>", methods=["GET", "POST"])
def accept_admin_invite(token):
    invite = AdminInvite.query.filter_by(token=token, used=False).first_or_404()
    form = ResetPasswordForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=invite.email.lower()).first()

        if existing_user:
            existing_user.role = "admin"
            existing_user.set_password(form.password.data)
        else:
            admin_user = User(
                name=invite.email.split("@")[0],
                email=invite.email.lower(),
                role="admin",
            )
            admin_user.set_password(form.password.data)
            db.session.add(admin_user)

        invite.used = True
        db.session.commit()

        flash("Adminbruker er opprettet. Du kan logge inn.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/accept_admin_invite.html", form=form, invite=invite)
