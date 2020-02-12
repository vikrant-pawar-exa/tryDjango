from flask import Flask

from app.api.api import main_api_blueprint
from app.api.auth import auth_bp

app = Flask(__name__)

app.config.from_object('config')

default_api_url = "/api"

app.register_blueprint(main_api_blueprint, url_prefix=default_api_url)
app.register_blueprint(auth_bp, url_prefix=default_api_url)

@app.errorhandler(404)
def page_not_found(error):
  return "This api not available....use /api"