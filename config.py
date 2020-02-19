class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME_GIT = ""
    PASSWORD_GIT = ""
    HOST_GIT = "exabeam.atlassian.net"


class ProductionConfig(Config):
    DATABASE_URI = 'mongo://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    TESTING = True