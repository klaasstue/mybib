from os import environ
from flask import Flask
import config as g

app = Flask(__name__, static_folder=g.static_folder, template_folder=g.template_folder)
app.config.from_object( environ['APP_SETTINGS'] )

import views
from catalog import Catalog

