from flask import Flask, request
from app.utils.custom_response import make_resp
import logging, requests, sys
from config import Config
from app.models.users import Users

def verify_okta_token(req_headers):
  try:
    if 'api-accessToken' not in req_headers:
      return make_resp({"message":"API token must be present"}, 404)
    else:
      api_token = req_headers.get('api-accessToken')
      api_token_list = api_token.split(' ')
      if len(api_token_list) != 2:
        return make_resp({"message":"Token invalid"}, 401)
      elif api_token_list[0].lower() != 'bearer':
        return make_resp({"message":"Token invalid"}, 401)
      else:
        resp_info = okta_user_info(api_token)
        if resp_info == None:
          return make_resp({"message":"Exception in API"}, 422)
        elif resp_info.status_code != requests.codes.ok:
          return make_resp({"message":"Invalid credentials"}, resp_info.status_code)
  except:
    logging.error("----Exception in OKTA API : {}".format(sys.exc_info()[1]))
    return make_resp({"message":"Exception in API: {}".format(sys.exc_info()[1])}, 422)


def okta_user_info(api_token):
  try:
    okta_userinfo_url = "{}/oauth2/default/v1/userinfo".format(Config.OKTA_HOST_URL)
    headers = {'Content-Type':'application/json','Authorization': api_token}
    return requests.post(okta_userinfo_url, headers=headers)
  except:
    logging.error("----Exception in OKTA User info API : {}".format(sys.exc_info()[1]))

def get_user_tokens(api_token):
  try:
    resp_info = okta_user_info(api_token)
    if resp_info.status_code == requests.codes.ok:
      user_info = Users.get_user(resp_info.json()["email"])
      return { 
          "jira_username": user_info["jira_username"],
          "jira_token": user_info["jira_token"],
          "git_username": user_info["git_username"],
          "git_token": user_info['git_token']
        }
    else:
      logging.error("----Exception in okta user info : {}".format(resp_info.status_code))
  except:
    logging.error("----Exception in getting user tokens from DB : {}".format(sys.exc_info()[1]))

