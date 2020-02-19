class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mongo://user@localhost/foo'
    OKTA_HOST_URL = 'https://dev-780755.okta.com'
class DevelopmentConfig(Config):
    DEBUG = True
    OKTA_HOST_URL = 'https://dev-780755.okta.com'

class StagingConfig(Config):
    TESTING = True