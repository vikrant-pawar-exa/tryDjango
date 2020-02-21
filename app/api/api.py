from flask import Blueprint, request, jsonify
from flask import Blueprint
from app.utils.custom_response import make_resp
from flask_restful import reqparse, abort, Api, Resource

from app.api.external.jira import *
from app.api.user_profiles import *
from app.test_cases.sbt import sbt_resource


main_api_blueprint = Blueprint('main_api_blueprint', __name__)

api = Api(main_api_blueprint)

@main_api_blueprint.route('/')
def index():
  return make_resp({"message":"api working"})

api.add_resource(sbt_resource, '/sbt/<ticket_id>')
api.add_resource(TicketUnresolved, '/tickets/unresolve_ticket')
api.add_resource(Ticket, '/tickets', endpoint="tickets")
api.add_resource(Comments, '/comments/<issueIdOrKey>')
api.add_resource(UpdateComments, '/comments/<issueIdOrKey>/<commentId>',methods=['PUT'])
api.add_resource(Attachment, '/attach/<issueIdOrKey>', methods=['POST'])
api.add_resource(UserProfile, '/users', methods=['POST', 'GET'])