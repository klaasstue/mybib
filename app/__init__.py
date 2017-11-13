from os import environ
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config as g

app = Flask(__name__, static_folder=g.static_folder, template_folder=g.template_folder)
app.config.from_object( environ['APP_SETTINGS'] )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import views, model, auth
from catalog import Catalog

