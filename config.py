class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME_GIT = ""
    PASSWORD_GIT = ""
    HOST_GIT = "exabeam.atlassian.net"
    EXA_SECURITY = ""


class ProductionConfig(Config):
    OKTA_HOST_URL = 'https://dev-780755.okta.com'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    OKTA_HOST_URL = 'https://dev-780755.okta.com'


class StagingConfig(Config):
    TESTING = True
