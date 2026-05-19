from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class LoginForm(FlaskForm):
    email = EmailField(
        "E-post",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    password = PasswordField(
        "Passord",
        validators=[
            DataRequired(),
            Length(min=8, max=128),
        ],
    )

    submit = SubmitField("Logg inn")


class AdminInviteForm(FlaskForm):
    email = EmailField(
        "Ny admin e-post",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    submit = SubmitField("Inviter admin")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Nytt passord",
        validators=[
            DataRequired(),
            Length(min=8, max=128),
        ],
    )

    confirm_password = PasswordField(
        "Bekreft passord",
        validators=[
            DataRequired(),
            EqualTo("password"),
        ],
    )

    submit = SubmitField("Oppdater passord")


class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        "E-post",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    submit = SubmitField("Send tilbakestillingslenke")


class EditProfileForm(FlaskForm):
    name = StringField(
        "Navn",
        validators=[
            DataRequired(),
            Length(min=2, max=120),
        ],
    )

    phone = StringField(
        "Telefonnummer",
        validators=[
            DataRequired(),
            Length(min=8, max=40),
        ],
    )

    submit = SubmitField("Lagre endringer")
