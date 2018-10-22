import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' \
                                        + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
#must be done after db
from aciapps.moquery.views import moquery_blueprints, create_blueprints
from aciapps.aepg_assignment.views import aepg_blueprints
app.register_blueprint(aepg_blueprints,url_prefix='/aepg')
app.register_blueprint(moquery_blueprints,url_prefix='/moquery')
app.register_blueprint(create_blueprints,url_prefix='/create')