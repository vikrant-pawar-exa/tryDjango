class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME_GIT = ""
    PASSWORD_GIT = ""
    HOST_GIT = "exabeam.atlassian.net"



class ProductionConfig(Config):
    DB_HOST = 'mongo://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = 'mongo://localhost:27017'
    OKTA_HOST_URL = 'https://dev-780755.okta.com'

class DevelopmentConfig(Config):
    DEBUG = True
    OKTA_HOST_URL = 'https://dev-780755.okta.com'

class StagingConfig(Config):
    TESTING = True
    DB_HOST = 'mongo://user@localhost/foo'
