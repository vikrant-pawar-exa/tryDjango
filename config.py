class Config(object):
    DEBUG = False
    TESTING = False
    HOST_JIRA = "exabeam.atlassian.net"
    DB_HOST = "mongodb://db:27017"
    OKTA_HOST_URL = 'https://dev-780755.okta.com'
    GIT = {
      "HOST": "https://api.github.com",
      "OWNER": "Test-GS-Lab", # "Exabeam"
      "REPO": "testing-org-repo", # "exa_security"
      "DEST_REPO_DIR": "exa_temp_repo",
      "DEFAULT_BRANCH": "CONT-0001"
    }
    EXA_SECURITY = "/home/exa_security"


    EXABEAM_HOME ="/test/exa_security/martini/"
    WORK_DIR ='/home/tickets'
    SMB_logs ='/secure/samba'
    FETCH_CSV_SCRIPT ="/opt/exabeam/scripts/FetchColCSV.py"
    MAKE_SPLUNKCSV_SCRIPT ="/opt/exabeam/scripts/make_SplunkCSV.sh"

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

