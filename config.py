class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME_GIT = "akshay.pange@exabeam.com"
    PASSWORD_GIT = "08wmmbS7IVY6n9f1pUGiAB04"
    HOST_GIT = "exabeam.atlassian.net"


class ProductionConfig(Config):
    DATABASE_URI = 'mongo://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    TESTING = True