class Config(object):
    DEBUG = False
    TESTING = False
    HOST_JIRA = "exabeam.atlassian.net"
    DB_HOST = "mongodb://db:27017"
    OKTA_HOST_URL = 'https://dev-152236.okta.com'
    EXA_SECURITY = "/home/exa_security"


    # EXABEAM_HOME ="/test/exa_security/martini/"
    EXABEAM_HOME = EXA_SECURITY + "/martini"
    WORK_DIR ='/home/tickets'
    SMB_logs ='/secure/samba'
    # FETCH_CSV_SCRIPT = EXA_SECURITY + "/Scripts/FetchColCSV.py"
    FETCH_CSV_SCRIPT ="/opt/exabeam/scripts/FetchColCSV.py"
    # MAKE_SPLUNKCSV_SCRIPT = EXA_SECURITY + "/scripts/make_SplunkCSV.sh"
    MAKE_SPLUNKCSV_SCRIPT ="/opt/exabeam/scripts/make_SplunkCSV.sh"

class ProductionConfig(Config):
    DB_HOST = 'mongo://user@localhost/foo'
    OKTA_HOST_URL = 'https://dev-152236.okta.com'


class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = 'mongo://localhost:27017'
    TESTING = True
    OKTA_HOST_URL = 'https://dev-152236.okta.com'
# Removing duplicated
# class DevelopmentConfig(Config):
#     DEBUG = True
#     OKTA_HOST_URL = 'https://dev-152236.okta.com'

class StagingConfig(Config):
    TESTING = True
    DB_HOST = 'mongo://user@localhost/foo'

