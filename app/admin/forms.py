from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional,
)

from wtforms.fields import EmailField


class AdminRegistrationEditForm(FlaskForm):
    contact_name = StringField(
        "Kontaktperson",
        validators=[
            DataRequired(),
            Length(min=2, max=120),
        ],
    )

    email = EmailField(
        "E-post",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    phone = StringField(
        "Telefonnummer",
        validators=[
            DataRequired(),
            Length(min=8, max=40),
        ],
    )

    adults_count = IntegerField(
        "Antall voksne",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=50),
        ],
    )

    children_under_10_count = IntegerField(
        "Barn under 10 år",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=50),
        ],
    )

    allergies = TextAreaField(
        "Allergier",
        validators=[
            Optional(),
            Length(max=1000),
        ],
    )

    overnight = SelectField(
        "Overnatting",
        validators=[DataRequired()],
        choices=[
            ("home", "Drar hjem"),
            ("self", "Ordner selv"),
            ("need_help", "Trenger at dere ordner"),
        ],
    )

    event_choice = SelectField(
        "Arrangement",
        validators=[DataRequired()],
        choices=[
            ("day", "Kun grilling"),
            ("evening", "Kun kveld"),
            ("both", "Begge"),
        ],
    )

    is_active = BooleanField("Aktiv påmelding")

    submit = SubmitField("Lagre")


class SiteContentForm(FlaskForm):
    title_no = StringField(
        "Norsk tittel",
        validators=[
            DataRequired(),
            Length(max=255),
        ],
    )

    body_no = TextAreaField(
        "Norsk tekst",
        validators=[
            DataRequired(),
        ],
    )

    title_en = StringField(
        "English title",
        validators=[
            DataRequired(),
            Length(max=255),
        ],
    )

    body_en = TextAreaField(
        "English text",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Lagre innhold")


class FilterForm(FlaskForm):
    event_choice = SelectField(
        "Arrangement",
        validators=[Optional()],
        choices=[
            ("", "Alle"),
            ("day", "Kun grilling"),
            ("evening", "Kun kveld"),
            ("both", "Begge"),
        ],
    )

    overnight = SelectField(
        "Overnatting",
        validators=[Optional()],
        choices=[
            ("", "Alle"),
            ("home", "Drar hjem"),
            ("self", "Ordner selv"),
            ("need_help", "Trenger hjelp"),
        ],
    )

    submit = SubmitField("Filtrer")
