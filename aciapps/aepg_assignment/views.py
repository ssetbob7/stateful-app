from aciapps import app
from aciapps.aepg_assignment.forms import AEPForm
from flask import render_template, Blueprint, redirect, url_for

aepg_blueprints = Blueprint('aepg', __name__, template_folder='templates')

@aepg_blueprints.route('/wtf', methods=['POST','GET'])
def wtf():
    form = AEPForm()
    if form.validate_on_submit():
        print(form.mselect.data)
    return render_template('wtf.html', form=form)

@aepg_blueprints.route('/endpoint', methods=['POST','GET'])
def endpoint():
  #  if 'username' not in session:
  #      return redirect(url_for('login'))
    return render_template('endpoint.html')