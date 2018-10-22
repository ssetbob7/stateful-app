from aciapps import db
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class AEPForm(FlaskForm):
    leaflist = [('leaf1', 'leaf1'),('leaf2', 'leaf2'),('leaf3', 'leaf3'),('leaf4', 'leaf4')]
    leafselect = SelectMultipleField('leafs', validators=[DataRequired(message='Hi')], choices=leaflist)
    leaflist = [('leaf1', 'leaf1'),('leaf2', 'leaf2'),('leaf3', 'leaf3'),('leaf4', 'leaf4')]
    ifselect = SelectMultipleField('interfaces', validators=[DataRequired(message='Hi')], choices=[('cp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

#    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('submit')