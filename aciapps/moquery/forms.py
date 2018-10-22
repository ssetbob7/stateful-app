from aciapps import db
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField
from wtforms.validators import DataRequired

class QueryACI(FlaskForm):
    search = StringField('Enter Class: ', validators=[(DataRequired(message='Username Required'))])
    submit = SubmitField('submit')

class CreateTenantTree(FlaskForm):
    tenant = StringField('Tenant', validators=[DataRequired(message='Tenant Required')])
    app = StringField('APP', validators=[DataRequired(message='APP required')])
    epg = StringField('EPG(s)', validators=[DataRequired(message='EPG Required')])
    bd = StringField('BD', validators=[DataRequired(message='BD Required')])
    