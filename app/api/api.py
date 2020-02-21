from flask import Blueprint
from app.utils.custom_response import make_resp
from flask_restful import reqparse, abort, Api, Resource
from config import Config

from app.api.external.jira import *
from app.test_cases.sbt import sbt_resource
from app.api.user import *

from app.test_cases.manual_steps import Lime

main_api_blueprint = Blueprint('main_api_blueprint', __name__)

api = Api(main_api_blueprint)


@main_api_blueprint.route('/')
def index():
  return make_resp({"message":"api working"})

api.add_resource(OktaUserInfo, '/users/user_info')
api.add_resource(sbt_resource, '/sbt/<ticket_id>')
api.add_resource(TicketUnresolved, '/tickets/unresolve_ticket')
api.add_resource(Ticket, '/tickets', endpoint="tickets")
api.add_resource(Comments, '/comments/<issueIdOrKey>')
api.add_resource(UpdateComments, '/comments/<issueIdOrKey>/<commentId>',methods=['PUT'])
api.add_resource(Attachment, '/attach/<issueIdOrKey>', methods=['POST'])

#Lime api
api.add_resource(Lime, '/lime/setup', methods=['POST'])
