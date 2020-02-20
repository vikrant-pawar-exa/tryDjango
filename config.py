class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DB_HOST = 'mongo://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = 'mongo://localhost:27017'

class StagingConfig(Config):
    TESTING = True
    DB_HOST = 'mongo://user@localhost/foo'
