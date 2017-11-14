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
#    SQLALCHEMY_DATABASE_URI = 'postgres://snejfynfkamndr:e1e52fad2b620327b2c96486dae0fbff21ed90f4868b45e0642bb58a87b1624b@ec2-107-20-195-181.compute-1.amazonaws.com:5432/d274hkqapbq4ra'
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'metadata.db')

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    BIBLIOTHEK = os.environ['BIBLIOTHEK']
    CALIBREDIR = "%s/.calibre" % os.environ['HOME']


class TestingConfig(Config):
    TESTING = True

