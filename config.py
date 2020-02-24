class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME_JIRA = ""
    PASSWORD_JIRA = ""
    HOST_JIRA = "exabeam.atlassian.net"
    DB_HOST = "mongodb://db:27017"
    OKTA_HOST_URL = 'https://dev-780755.okta.com'
    EXA_SECURITY = ""



class ProductionConfig(Config):
    DB_HOST = 'mongo://user@localhost/foo'

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

