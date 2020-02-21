from flask import Blueprint, request, jsonify
from flask import Blueprint
from app.utils.custom_response import make_resp
from flask_restful import reqparse, abort, Api, Resource

from app.api.external.jira import *
from app.api.user_profiles import *
from app.test_cases.sbt import sbt_resource
from app.api.user import *


main_api_blueprint = Blueprint('main_api_blueprint', __name__)

api = Api(main_api_blueprint)

@main_api_blueprint.route('/')
def index():
  return make_resp({"message":"Api working -: This is exceptional routes that don't required token"})


api.add_resource(OktaUserInfo, '/users/user_info')
api.add_resource(sbt_resource, '/sbt/<ticket_id>')
api.add_resource(TicketUnresolved, '/ticket/unresolve_ticket')
api.add_resource(Ticket, '/ticket')
api.add_resource(Comments, '/ticket/<issueIdOrKey>/comments')
api.add_resource(UpdateComments, '/ticket/<issueIdOrKey>/comments/<commentId>',methods=['PUT'])
api.add_resource(Transition, '/ticket/<issueIdOrKey>/transition', methods=['POST', 'GET'])
api.add_resource(Attachment, '/ticket/<issueIdOrKey>/attach', methods=['POST'])
api.add_resource(UserProfile, '/users', methods=['POST', 'GET'])

