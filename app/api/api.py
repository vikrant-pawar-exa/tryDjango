from flask import Blueprint

main_api_blueprint = Blueprint('main_api_blueprint', __name__)

@main_api_blueprint.route('/')
def index():
  return "This is a main api ..."