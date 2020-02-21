class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME_JIRA = ""
    PASSWORD_JIRA = ""
    HOST_JIRA = "exabeam.atlassian.net"
    OKTA_HOST_URL = 'https://dev-780755.okta.com'
    EXA_SECURITY = ""


    EXABEAM_HOME = "/test/exa_security/martini/"
    WORK_DIR = '/test/dataInput/'
    TICKETS_DIR_PATH ='/opt/samba/secured'
    FETCH_CSV_SCRIPT = "/opt/exabeam/scripts/FetchColCSV.py"
    MAKE_SPLUNKCSV_SCRIPT = "/opt/exabeam/scripts/make_SplunkCSV.sh"

class ProductionConfig(Config):
    OKTA_HOST_URL = 'https://dev-780755.okta.com'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    OKTA_HOST_URL = 'https://dev-780755.okta.com'


class StagingConfig(Config):
    TESTING = True
