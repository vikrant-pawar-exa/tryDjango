class Config(object):
    DEBUG = False
    TESTING = False
    HOST_JIRA = "exabeam.atlassian.net"

    OKTA_HOST_URL = 'https://dev-780755.okta.com'
    EXA_SECURITY = "/home/vikrant/exa_security"


class ProductionConfig(Config):
    DB_HOST = 'mongo://user@localhost/foo'
    OKTA_HOST_URL = 'https://dev-780755.okta.com'


class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = 'mongo://localhost:27017'
    TESTING = True
    OKTA_HOST_URL = 'https://dev-780755.okta.com'
# Removing duplicated
# class DevelopmentConfig(Config):
#     DEBUG = True
#     OKTA_HOST_URL = 'https://dev-780755.okta.com'

class StagingConfig(Config):
    TESTING = True
    DB_HOST = 'mongo://user@localhost/foo'

