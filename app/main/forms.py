from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


#forms

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('About')
    submit = SubmitField('Update Profile')

class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = TextAreaField('Leave a Comment', validators=[DataRequired()], render_kw={"rows": "7"})
    submit = SubmitField('Submit')

class PasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')