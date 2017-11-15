import os, json

basedir   = os.path.abspath( os.path.dirname(__file__) )
appdir    = os.path.join( basedir, 'app' )
static_folder   = os.path.join( basedir, 'ressources')
template_folder = os.path.join( basedir, 'templates')

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

