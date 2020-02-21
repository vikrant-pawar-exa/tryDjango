from flask import request
from flask_restful import Resource

from app.utils.user import okta_user_info

class OktaUserInfo(Resource):
  def post(self):
    resp_info = okta_user_info(request.headers.get('api-accessToken'))
    return (resp_info).json()
  