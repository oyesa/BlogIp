from flask_wtf import FlaskForm
from ..models import User
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 50)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def check_email_exist(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. Please Login')

    def check_username_exist(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')