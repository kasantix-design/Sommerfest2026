from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
)


class RegistrationForm(FlaskForm):
    contact_name = StringField(
        "Kontaktperson",
        validators=[DataRequired(), Length(min=2, max=120)],
    )

    email = EmailField(
        "E-post",
        validators=[DataRequired(), Email()],
    )

    phone = StringField(
        "Telefonnummer",
        validators=[DataRequired(), Length(min=8, max=40)],
    )

    password = PasswordField(
        "Passord",
        validators=[DataRequired(), Length(min=8, max=128)],
    )

    confirm_password = PasswordField(
        "Bekreft passord",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passordene må være like."),
        ],
    )

    adults_count = IntegerField(
        "Antall voksne",
        validators=[DataRequired(), NumberRange(min=1, max=50)],
        default=1,
    )

    children_under_10_count = IntegerField(
    "Barn under 10 år",
    validators=[NumberRange(min=0, max=50)],
    default=0,
    )

    allergies = TextAreaField(
        "Allergier",
        validators=[Optional(), Length(max=1000)],
    )

    arrival_time = TimeField(
        "Kommer fra",
        validators=[Optional()],
        format="%H:%M",
    )

    departure_time = TimeField(
        "Kommer til",
        validators=[Optional()],
        format="%H:%M",
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

    avatar = SelectField(
        "Avatar",
        validators=[Optional()],
        choices=[
            ("butterfly_pink", "🦋 Rosa sommerfugl"),
            ("butterfly_gold", "✨ Gullsommerfugl"),
            ("flower", "🌸 Blomst"),
            ("sun", "☀️ Sol"),
        ],
    )

    submit = SubmitField("Meld familien på")
