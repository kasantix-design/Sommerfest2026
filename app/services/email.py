from flask import current_app, url_for
from flask_mail import Message

from app.extensions import mail


def send_email(subject, recipients, body):
    mail_username = current_app.config.get("MAIL_USERNAME")

    if not mail_username:
        current_app.logger.warning("MAIL_USERNAME mangler. E-post ble ikke sendt.")
        return False

    try:
        message = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            sender=mail_username,
        )
        mail.send(message)
        return True

    except Exception as error:
        current_app.logger.exception("Kunne ikke sende e-post: %s", error)
        return False


def send_registration_emails(registration):
    private_link = url_for(
        "main.registration_by_token",
        private_token=registration.private_token,
        _external=True,
    )

    participant_body = f"""
Hei {registration.contact_name}!

Du er nå påmeldt Sommerfest 2026.

Antall voksne: {registration.adults_count}
Barn under 10 år: {registration.children_under_10_count}
Totalt antall: {registration.total_people}

Allergier: {registration.allergies or "Ingen oppgitt"}
Kommer fra: {registration.arrival_time or "Ikke oppgitt"}
Kommer til: {registration.departure_time or "Ikke oppgitt"}
Overnatting: {registration.overnight}
Arrangement: {registration.event_choice}

Du kan se påmeldingen din her:
{private_link}

Hilsen
Sommerfest 2026
"""

    admin_body = f"""
Ny påmelding til Sommerfest 2026:

Kontaktperson: {registration.contact_name}
E-post: {registration.email}
Telefon: {registration.phone}

Voksne: {registration.adults_count}
Barn under 10 år: {registration.children_under_10_count}
Totalt: {registration.total_people}

Allergier: {registration.allergies or "Ingen oppgitt"}
Kommer fra: {registration.arrival_time or "Ikke oppgitt"}
Kommer til: {registration.departure_time or "Ikke oppgitt"}
Overnatting: {registration.overnight}
Arrangement: {registration.event_choice}

Privat lenke:
{private_link}
"""

    send_email(
        subject="Du er påmeldt Sommerfest 2026",
        recipients=[registration.email],
        body=participant_body,
    )

    send_email(
        subject="Ny påmelding til Sommerfest 2026",
        recipients=[current_app.config.get("ADMIN_EMAIL", "kasantix@gmail.com")],
        body=admin_body,
    )


def send_registration_updated_emails(registration):
    participant_body = f"""
Hei {registration.contact_name}!

Påmeldingen din til Sommerfest 2026 er oppdatert.

Voksne: {registration.adults_count}
Barn under 10 år: {registration.children_under_10_count}
Totalt: {registration.total_people}

Hilsen
Sommerfest 2026
"""

    admin_body = f"""
En påmelding er oppdatert:

Kontaktperson: {registration.contact_name}
E-post: {registration.email}
Telefon: {registration.phone}
"""

    send_email(
        subject="Påmeldingen din er oppdatert",
        recipients=[registration.email],
        body=participant_body,
    )

    send_email(
        subject="En påmelding er oppdatert",
        recipients=[current_app.config.get("ADMIN_EMAIL", "kasantix@gmail.com")],
        body=admin_body,
    )


def send_registration_cancelled_emails(registration):
    participant_body = f"""
Hei {registration.contact_name}!

Du er nå avmeldt Sommerfest 2026.

Hilsen
Sommerfest 2026
"""

    admin_body = f"""
En familie har meldt seg av Sommerfest 2026:

Kontaktperson: {registration.contact_name}
E-post: {registration.email}
Telefon: {registration.phone}
"""

    send_email(
        subject="Du er avmeldt Sommerfest 2026",
        recipients=[registration.email],
        body=participant_body,
    )

    send_email(
        subject="En familie har meldt seg av",
        recipients=[current_app.config.get("ADMIN_EMAIL", "kasantix@gmail.com")],
        body=admin_body,
    )
