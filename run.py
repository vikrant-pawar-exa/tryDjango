from flask import Flask
from config import Config
import logging

from app.api.api import main_api_blueprint
from app.api.auth import auth_bp

app = Flask(__name__)

app.config.from_object(Config)

logging.basicConfig(filename='log/development.log',level=logging.DEBUG)

logging.info("{}".format(app.config))



# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

default_api_url = "/api"

app.register_blueprint(main_api_blueprint, url_prefix=default_api_url)
app.register_blueprint(auth_bp, url_prefix=default_api_url)

@app.errorhandler(404)
def page_not_found(error):
  return "This api not available....use /api"
