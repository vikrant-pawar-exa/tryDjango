class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME_JIRA = ""
    PASSWORD_JIRA = ""
    HOST_JIRA = "exabeam.atlassian.net"

    OKTA_HOST_URL = 'https://dev-780755.okta.com'
    EXA_SECURITY = ""


class ProductionConfig(Config):
    OKTA_HOST_URL = 'https://dev-780755.okta.com'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    OKTA_HOST_URL = 'https://dev-780755.okta.com'


class StagingConfig(Config):
    TESTING = True
