import click
from flask import Flask

from app.extensions import db
from app.models import SiteContent, User


def register_cli(app: Flask) -> None:
    @app.cli.command("seed")
    def seed_database():
        admins = [
            {
                "name": "Reidun",
                "email": "kasantix@gmail.com",
                "phone": "41646966",
                "password": "ChangeMe2026!",
            },
            {
                "name": "Lars",
                "email": "lksandvik@pm.me",
                "phone": "93224759",
                "password": "ChangeMe2026!",
            },
        ]

        for admin in admins:
            user = User.query.filter_by(email=admin["email"].lower()).first()

            if not user:
                user = User(
                    name=admin["name"],
                    email=admin["email"].lower(),
                    phone=admin["phone"],
                    role="admin",
                )
                user.set_password(admin["password"])
                db.session.add(user)
            else:
                user.role = "admin"
                user.phone = admin["phone"]
                user.set_password(admin["password"])

        if not SiteContent.query.filter_by(key="hero").first():
            db.session.add(SiteContent(
                key="hero",
                title_no="Sommerfest i hagen på Hop",
                body_no="Lars og Reidun feirer 30 års bryllupsdag.",
                title_en="Summer party in the garden at Hop",
                body_en="Lars and Reidun are celebrating their 30th wedding anniversary.",
            ))

        if not SiteContent.query.filter_by(key="practical").first():
            db.session.add(SiteContent(
                key="practical",
                title_no="Praktisk informasjon",
                body_no="Grilling kl. 15–19. Kveldskos kl. 20–00. Adresse: Østre Hopsvegen 3a, 5232 Paradis.",
                title_en="Practical information",
                body_en="Barbecue 15–19. Evening gathering 20–00. Address: Østre Hopsvegen 3a, 5232 Paradis.",
            ))

        db.session.commit()

        click.echo("Seed ferdig.")
        click.echo("Admin Reidun: kasantix@gmail.com / ChangeMe2026!")
        click.echo("Admin Lars: lksandvik@pm.me / ChangeMe2026!")
