class Config(object):
    FLASK_APP='run.py'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mongo://user@localhost/foo'

class ProductionConfig(Config):
    DATABASE_URI = 'mongo://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class StagingConfig(Config):
    TESTING = True