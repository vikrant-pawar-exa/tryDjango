class Config(object):
    DEBUG = False
    TESTING = False
    HOST_JIRA = "exabeam.atlassian.net"
    DB_HOST = "mongodb://db:27017"
    OKTA_HOST_URL = 'https://dev-780755.okta.com'
    EXA_SECURITY = ""
    GIT = {
      "HOST": "https://api.github.com",
      "OWNER": "Test-GS-Lab", # "Exabeam"
      "REPO": "testing-org-repo", # "exa_security"
      "DEST_REPO_DIR": "exa_temp_repo",
      "DEFAULT_BRANCH": "CONT-0001"
    }

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

