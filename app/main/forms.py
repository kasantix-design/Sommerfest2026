from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.fields import TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Optional


class RegistrationForm(FlaskForm):
    contact_name = StringField('Contact Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    avatar = StringField('Avatar', validators=[Optional()])
    password = PasswordField('Password', validators=[Optional(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password')
    adults_count = IntegerField('Adults', validators=[DataRequired()])
    children_under_10_count = IntegerField('Children under 10', validators=[Optional()])
    allergies = TextAreaField('Allergies', validators=[Optional()])
    arrival_time = TimeField('Arrival time', validators=[Optional()])
    departure_time = TimeField('Departure time', validators=[Optional()])
    overnight = BooleanField('Overnight')
    event_choice = SelectField('Event choice', choices=[('day', 'Day'), ('evening', 'Evening')], validators=[Optional()])
    submit = SubmitField('Submit')
