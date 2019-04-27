from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flaskblog.db import validate

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(),
                                Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        result = validate('username', username.data)
        if result:
            raise ValidationError('That username is already taken. Please choose a new one!')
    
    def validate_email(self, email):
        result = validate('email', email.data)
        if result:
            raise ValidationError('That email is already registered. Please login!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')