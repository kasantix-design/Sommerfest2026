import csv
from io import BytesIO, StringIO

from flask import (
    Blueprint,
    Response,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required
from openpyxl import Workbook

from app.admin.forms import AdminRegistrationEditForm, FilterForm, SiteContentForm
from app.auth.forms import AdminInviteForm
from app.extensions import db
from app.models import AdminInvite, Registration, SiteContent, User

admin_bp = Blueprint("admin", __name__)


def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)


@admin_bp.before_request
def protect_admin_routes():
    admin_required()


@admin_bp.route("/")
def dashboard():
    filter_form = FilterForm(request.args)

    query = Registration.query.order_by(Registration.created_at.desc())

    event_choice = request.args.get("event_choice")
    overnight = request.args.get("overnight")
    allergies = request.args.get("allergies")
    children = request.args.get("children")

    if event_choice:
        query = query.filter_by(event_choice=event_choice)

    if overnight:
        query = query.filter_by(overnight=overnight)

    if allergies == "yes":
        query = query.filter(Registration.allergies.isnot(None))

    if children == "yes":
        query = query.filter(Registration.children_under_10_count > 0)

    registrations = query.all()

    return render_template(
        "admin/dashboard.html",
        registrations=registrations,
        filter_form=filter_form,
    )


@admin_bp.route("/pamelding/<int:registration_id>/rediger", methods=["GET", "POST"])
def edit_registration(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    form = AdminRegistrationEditForm(obj=registration)

    if form.validate_on_submit():
        registration.contact_name = form.contact_name.data.strip()
        registration.email = form.email.data.lower().strip()
        registration.phone = form.phone.data.strip()
        registration.adults_count = form.adults_count.data
        registration.children_under_10_count = form.children_under_10_count.data
        registration.allergies = form.allergies.data
        registration.overnight = form.overnight.data
        registration.event_choice = form.event_choice.data
        registration.is_active = form.is_active.data

        registration.user.name = registration.contact_name
        registration.user.email = registration.email
        registration.user.phone = registration.phone

        db.session.commit()

        flash("Påmeldingen er oppdatert.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/edit_registration.html",
        form=form,
        registration=registration,
    )


@admin_bp.route("/pamelding/<int:registration_id>/slett", methods=["POST"])
def delete_registration(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    user = registration.user

    db.session.delete(user)
    db.session.commit()

    flash("Påmeldingen er slettet.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/eksport/csv")
def export_csv():
    registrations = Registration.query.order_by(Registration.created_at.desc()).all()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "Kontaktperson",
            "E-post",
            "Telefon",
            "Voksne",
            "Barn under 10",
            "Totalt",
            "Allergier",
            "Kommer fra",
            "Kommer til",
            "Overnatting",
            "Arrangement",
            "Aktiv",
            "Registrert",
        ]
    )

    for registration in registrations:
        writer.writerow(
            [
                registration.contact_name,
                registration.email,
                registration.phone,
                registration.adults_count,
                registration.children_under_10_count,
                registration.total_people,
                registration.allergies or "",
                registration.arrival_time or "",
                registration.departure_time or "",
                registration.overnight,
                registration.event_choice,
                "Ja" if registration.is_active else "Nei",
                registration.created_at,
            ]
        )

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=sommerfest-2026.csv"
        },
    )


@admin_bp.route("/eksport/excel")
def export_excel():
    registrations = Registration.query.order_by(Registration.created_at.desc()).all()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Påmeldinger"

    sheet.append(
        [
            "Kontaktperson",
            "E-post",
            "Telefon",
            "Voksne",
            "Barn under 10",
            "Totalt",
            "Allergier",
            "Kommer fra",
            "Kommer til",
            "Overnatting",
            "Arrangement",
            "Aktiv",
            "Registrert",
        ]
    )

    for registration in registrations:
        sheet.append(
            [
                registration.contact_name,
                registration.email,
                registration.phone,
                registration.adults_count,
                registration.children_under_10_count,
                registration.total_people,
                registration.allergies or "",
                registration.arrival_time or "",
                registration.departure_time or "",
                registration.overnight,
                registration.event_choice,
                "Ja" if registration.is_active else "Nei",
                str(registration.created_at),
            ]
        )

    file_stream = BytesIO()
    workbook.save(file_stream)
    file_stream.seek(0)

    return send_file(
        file_stream,
        as_attachment=True,
        download_name="sommerfest-2026.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@admin_bp.route("/innhold/<key>", methods=["GET", "POST"])
def edit_content(key):
    content = SiteContent.query.filter_by(key=key).first_or_404()
    form = SiteContentForm(obj=content)

    if form.validate_on_submit():
        content.title_no = form.title_no.data
        content.body_no = form.body_no.data
        content.title_en = form.title_en.data
        content.body_en = form.body_en.data

        db.session.commit()

        flash("Innholdet er oppdatert.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_content.html", form=form, content=content)


@admin_bp.route("/inviter-admin", methods=["GET", "POST"])
def invite_admin():
    form = AdminInviteForm()

    if form.validate_on_submit():
        invite = AdminInvite(email=form.email.data.lower().strip())
        db.session.add(invite)
        db.session.commit()

        invite_link = url_for(
            "auth.accept_admin_invite",
            token=invite.token,
            _external=True,
        )

        flash(f"Admin-invitasjon opprettet: {invite_link}", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/invite_admin.html", form=form)
