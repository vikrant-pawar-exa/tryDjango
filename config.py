class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME_JIRA = ""
    PASSWORD_JIRA = ""
    HOST_JIRA = ""


class ProductionConfig(Config):
    DATABASE_URI = 'mongo://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    TESTING = True