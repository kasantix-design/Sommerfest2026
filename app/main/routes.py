from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user

from app.extensions import db
from app.main.forms import RegistrationForm
from app.models import Registration, SiteContent, User
from app.services.email import (
    send_registration_cancelled_emails,
    send_registration_emails,
    send_registration_updated_emails,
)


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    hero = SiteContent.query.filter_by(key='hero').first()
    practical = SiteContent.query.filter_by(key='practical').first()
    return render_template('main/index.html', hero=hero, practical=practical)


@main_bp.route('/registrer', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if existing_user:
            flash('Det finnes allerede en konto med denne e-posten.', 'warning')
            return redirect(url_for('auth.login'))

        user = User(
            name=form.contact_name.data.strip(),
            email=form.email.data.lower().strip(),
            phone=form.phone.data.strip(),
            role='family',
            avatar=form.avatar.data,
        )
        user.set_password(form.password.data)

        registration = Registration(
            user=user,
            contact_name=form.contact_name.data.strip(),
            email=form.email.data.lower().strip(),
            phone=form.phone.data.strip(),
            adults_count=form.adults_count.data,
            children_under_10_count=form.children_under_10_count.data,
            allergies=form.allergies.data,
            arrival_time=(
                form.arrival_time.data.strftime('%H:%M')
                if form.arrival_time.data
                else None
            ),
            departure_time=(
                form.departure_time.data.strftime('%H:%M')
                if form.departure_time.data
                else None
            ),
            overnight=form.overnight.data,
            event_choice=form.event_choice.data,
            is_active=True,
        )

        db.session.add(user)
        db.session.add(registration)
        db.session.commit()

        send_registration_emails(registration)

        login_user(user)

        flash('Du er nå påmeldt! Valgt arrangement er markert grønt.', 'success')
        return redirect(url_for('main.my_registration'))

    return render_template('main/register.html', form=form)


@main_bp.route('/min-pamelding')
@login_required
def my_registration():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))

    registration = current_user.registration
    if not registration:
        flash('Vi fant ingen påmelding på kontoen din.', 'warning')
        return redirect(url_for('main.register'))

    return render_template('main/my_registration.html', registration=registration)


@main_bp.route('/pamelding/<private_token>')
def registration_by_token(private_token):
    registration = Registration.query.filter_by(private_token=private_token).first_or_404()
    return render_template('main/my_registration.html', registration=registration)


@main_bp.route('/rediger-pamelding', methods=['GET', 'POST'])
@login_required
def edit_registration():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))

    registration = current_user.registration
    if not registration:
        abort(404)

    form = RegistrationForm(obj=registration)
    form.password.validators = []

    if request.method == 'GET':
        form.contact_name.data = registration.contact_name
        form.email.data = registration.email
        form.phone.data = registration.phone
        form.adults_count.data = registration.adults_count
        form.children_under_10_count.data = registration.children_under_10_count
        form.allergies.data = registration.allergies
        form.overnight.data = registration.overnight
        form.event_choice.data = registration.event_choice
        form.avatar.data = current_user.avatar

    if form.validate_on_submit():
        registration.contact_name = form.contact_name.data.strip()
        registration.email = form.email.data.lower().strip()
        registration.phone = form.phone.data.strip()
        registration.adults_count = form.adults_count.data
        registration.children_under_10_count = form.children_under_10_count.data
        registration.allergies = form.allergies.data
        registration.arrival_time = (
            form.arrival_time.data.strftime('%H:%M')
            if form.arrival_time.data
            else None
        )
        registration.departure_time = (
            form.departure_time.data.strftime('%H:%M')
            if form.departure_time.data
            else None
        )
        registration.overnight = form.overnight.data
        registration.event_choice = form.event_choice.data

        current_user.name = registration.contact_name
        current_user.email = registration.email
        current_user.phone = registration.phone
        current_user.avatar = form.avatar.data

        db.session.commit()

        send_registration_updated_emails(registration)

        flash('Påmeldingen er oppdatert.', 'success')
        return redirect(url_for('main.my_registration'))

    return render_template('main/edit_registration.html', form=form, registration=registration)


@main_bp.route('/avmeld', methods=['POST'])
@login_required
def cancel_registration():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))

    registration = current_user.registration
    if not registration:
        abort(404)

    confirm = request.form.get('confirm')
    if confirm != 'yes':
        flash('Avmelding ble ikke bekreftet.', 'warning')
        return redirect(url_for('main.my_registration'))

    registration.is_active = False
    db.session.commit()

    send_registration_cancelled_emails(registration)

    flash('Du er nå avmeldt.', 'success')
    return redirect(url_for('main.my_registration'))


@main_bp.route('/personvern')
def privacy():
    return render_template('main/privacy.html')


@main_bp.route('/kontakt')
def contact():
    return render_template('main/contact.html')


@main_bp.route('/faq')
def faq():
    return render_template('main/faq.html')


@main_bp.route('/offline')
def offline():
    return render_template('main/offline.html')
