class Config(object):
    AB="AMOL"
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mongo://user@localhost/foo'
    AB="PROD"
class DevelopmentConfig(Config):
    DEBUG = True

class StagingConfig(Config):
    TESTING = True