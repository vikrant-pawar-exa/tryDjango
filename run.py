from flask import Flask, request
from config import Config, ProductionConfig, DevelopmentConfig
import logging, requests, sys
from flask_restful import Api

from app.api.api import main_api_blueprint
from app.api.auth import auth_bp
from app.utils.custom_response import make_resp

app = Flask("CA_backend")

if app.config["ENV"] == "production":
  app.config.from_object(ProductionConfig)
  logging.basicConfig(filename='log/production.log',level=logging.INFO)
else:
  app.config.from_object(DevelopmentConfig)
  logging.basicConfig(filename='log/development.log',level=logging.DEBUG)


@app.before_request
def verify_access_token():
  try:
    if 'api-accessToken' not in request.headers:
      return make_resp({"message":"API token must be present"}, 404)
    else:
      api_token = request.headers.get('api-accessToken')
      api_token_list = api_token.split(' ')
      if len(api_token_list) != 2:
        return make_resp({"message":"Token invalid"}, 401)
      elif api_token_list[0].lower() != 'bearer':
        return make_resp({"message":"Token invalid"}, 401)
      else:
        okta_userinfo_url = "{}/oauth2/default/v1/userinfo".format(app.config["OKTA_HOST_URL"])
        headers = {'Content-Type':'application/json','Authorization': api_token}
        resp_info = requests.post(okta_userinfo_url, headers=headers)
        if resp_info.status_code != requests.codes.ok:
          return make_resp({"message":"Invalid credentials"}, resp_info.status_code)
        else:
          logging.debug("------User--{}---Status---{}---".format(resp_info.json()["email"], resp_info))  
  except Exception as e:
    logging.error("----Exception in OKTA API : {}".format(sys.exc_info()[1]))
    return make_resp({"message":"Exception in API: {}".format(sys.exc_info()[1])}, 422)


default_api_url = "/api"
api = Api(app)

app.register_blueprint(main_api_blueprint, url_prefix=default_api_url)
app.register_blueprint(auth_bp, url_prefix=default_api_url)


@app.errorhandler(404)
def page_not_found(error):
  return make_resp({"message":"Api not found"}, 404)

if __name__ == '__main__':
  app.run(host="0.0.0.0")
