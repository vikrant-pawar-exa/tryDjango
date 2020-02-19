from flask import Blueprint
from app.utils.custom_response import make_resp

main_api_blueprint = Blueprint('main_api_blueprint', __name__)

@main_api_blueprint.route('/')
def index():
  return make_resp({"message":"api working"})