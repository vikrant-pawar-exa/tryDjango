from flask_restful import Resource
import requests, logging, os
from flask import request, jsonify, abort
from app.utils.custom_response import make_resp
from app.utils.constant import Constants
logger = logging.getLogger(__name__)

headersObj = {
  "Accept": "application/json",
  "Authorization":"token {}".format(Constants.GIT["ACCESS_TOKEN"])
}

class GitPullRequest(Resource):
  def get(self):
    try:
      resp = requests.get(Constants.GIT["PULL_REQUEST_URL"], headersObj)
      if resp.status_code == requests.codes.ok:
        resp_data = resp.json()
        # logger.debug("----REQ URL------------{}--".format(resp.json()))
        return make_resp({"result": resp_data})
      else:
        return make_resp({"message": "Error in response {}".format(resp.status_code) })
    except Exception as e:
      logger.debug("---Exception Git API {}------------------".format(e.args))
      return make_resp({"message": "Exception Git API {}".format(e.args)})
