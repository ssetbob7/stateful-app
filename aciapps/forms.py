from aciapps import db
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Email

class NewUser(FlaskForm):
    user = StringField('Username:', validators=[DataRequired(message='Username Required')])
    password = PasswordField('Password:', validators=[DataRequired(message='Passowrd Required')])
    email = StringField('Email:', validators=[DataRequired(message='Email Required'), Email(message='Invalid Email')])
    submit = SubmitField('submit')

class LoginUser(FlaskForm):
    user = StringField('Username:', validators=[DataRequired(message='Username Required')])
    password = PasswordField('Password:', validators=[DataRequired(message='Passowrd Required')])
    submit = SubmitField('submit')

class IPSearch(FlaskForm):
    ip = StringField('Enter IP route:', validators=[DataRequired(message='ip required')])
    submit = SubmitField('submit')
