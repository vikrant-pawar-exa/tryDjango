from flask import Flask, request
from config import Config, ProductionConfig, DevelopmentConfig
import logging, requests, sys
from flask_restful import Api
from flask_cors import CORS

from app.api.api import main_api_blueprint
from app.utils.custom_response import make_resp
from app.utils.user import verify_okta_token
from app.utils.constant import Constants

app = Flask("CA_backend")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if app.config["ENV"] == "production":
  app.config.from_object(ProductionConfig)
  logging.basicConfig(filename='log/production.log',level=logging.INFO)
else:
  app.config.from_object(DevelopmentConfig)
  logging.basicConfig(filename='log/development.log',level=logging.DEBUG)


@app.before_request
def verify_access_token():
  if request.path not in Constants.ROUTES_WITHOUT_TOKEN:
    return verify_okta_token(request.headers)

default_api_url = "/api"
api = Api(app)

app.register_blueprint(main_api_blueprint, url_prefix=default_api_url)

@app.errorhandler(404)
def page_not_found(error):
  return make_resp({"message":"Api not found"}, 404)

if __name__ == '__main__':
  app.run(host="0.0.0.0")
