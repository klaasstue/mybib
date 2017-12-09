from os import environ
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config as g, auth

app = Flask(__name__, static_folder=g.static_folder, template_folder=g.template_folder)
app.config.from_object( environ['APP_SETTINGS'] )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

DER_FILE = "bib.der"
_db = auth.load_user_data( DER_FILE )
authDB = auth.FlaskRealmDigestDB( 'PrivateLibraryRealm', db = _db )

import model, views
#from catalog import Catalog

