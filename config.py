import os, json

basedir   = os.path.abspath( os.path.dirname(__file__) )
appdir    = os.path.join( basedir, 'app' )
static_folder   = os.path.join( basedir, 'ressources')
template_folder = os.path.join( basedir, 'templates')


with open('base.json') as fp:
    entries = json.load(fp).values()

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
#    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'metadata.db')
    BIBLIOTHEK = os.environ['BIBLIOTHEK']

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

