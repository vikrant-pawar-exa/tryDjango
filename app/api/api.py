from flask import Blueprint
from flask_restful import reqparse, abort, Api, Resource
from app.test_cases.sbt import sbt_resource

main_api_blueprint = Blueprint('main_api_blueprint', __name__)


@main_api_blueprint.route('/')
def index():
    return "This is a main api ..."
api = Api(main_api_blueprint)

api.add_resource(sbt_resource, '/sbt/<ticket_id>')
