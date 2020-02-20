from flask import Blueprint
from app.utils.custom_response import make_resp
from flask_restful import reqparse, abort, Api, Resource

from app.api.external.jira import *
from app.test_cases.sbt import sbt_resource

main_api_blueprint = Blueprint('main_api_blueprint', __name__)

api = Api(main_api_blueprint)


@main_api_blueprint.route('/')
def index():
  return make_resp({"message":"api working"})

api.add_resource(sbt_resource, '/sbt/<ticket_id>')
api.add_resource(TicketUnresolved, '/ticket/unresolve_ticket')
api.add_resource(Ticket, '/ticket')
api.add_resource(Comments, '/ticket/<issueIdOrKey>/comments')
api.add_resource(UpdateComments, '/ticket/<issueIdOrKey>/comments/<commentId>',methods=['PUT'])
api.add_resource(Transition, '/ticket/<issueIdOrKey>/transition', methods=['POST', 'GET'])
api.add_resource(Attachment, '/ticket/<issueIdOrKey>/attach', methods=['POST'])

