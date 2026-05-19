import uuid
from datetime import datetime, timezone
from secrets import token_urlsafe

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(40), nullable=True)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False, default='family')
    avatar = db.Column(db.String(80), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    registration = db.relationship(
        'Registration',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan',
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == 'admin'


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    contact_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(40), nullable=False)

    adults_count = db.Column(db.Integer, nullable=False, default=1)
    children_under_10_count = db.Column(db.Integer, nullable=False, default=0)

    allergies = db.Column(db.Text, nullable=True)

    arrival_time = db.Column(db.String(10), nullable=True)
    departure_time = db.Column(db.String(10), nullable=True)

    overnight = db.Column(db.String(40), nullable=False, default='home')
    event_choice = db.Column(db.String(40), nullable=False, default='both')

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    private_token = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        default=lambda: token_urlsafe(32),
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship('User', back_populates='registration')

    @property
    def total_people(self) -> int:
        return self.adults_count + self.children_under_10_count


class SiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(80), unique=True, nullable=False)
    title_no = db.Column(db.String(255), nullable=False)
    body_no = db.Column(db.Text, nullable=False)
    title_en = db.Column(db.String(255), nullable=False)
    body_en = db.Column(db.Text, nullable=False)

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class AdminInvite(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), nullable=False, index=True)
    token = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        default=lambda: token_urlsafe(32),
    )
    used = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))
