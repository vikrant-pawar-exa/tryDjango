from flask import Blueprint
from flask_restful import Api
from app.api.external.jira import *
from app.api.testcase import test_case
from app.api.user import *
from app.test_cases.manual_steps import *
from app.api.user_profiles import *

main_api_blueprint = Blueprint('main_api_blueprint', __name__)

api = Api(main_api_blueprint)


@main_api_blueprint.route('/')
def index():
    return make_resp({"message": "Api working -: This is exceptional routes that don't required token"})


api.add_resource(OktaUserInfo, '/users/user_info')

api.add_resource(test_case, '/tests/<ticket_id>/<test_name>')
# /tests/CONT-1234/sbt will execute test sbt for CONT-1234
# api.add_resource(sbt_resource, '/sbt/<ticket_id>/getFile')


api.add_resource(TicketUnresolved, '/ticket/unresolve_ticket')
api.add_resource(Ticket, '/ticket')
api.add_resource(Comments, '/ticket/<issueIdOrKey>/comments')
api.add_resource(UpdateComments, '/ticket/<issueIdOrKey>/comments/<commentId>', methods=['PUT'])
api.add_resource(Transition, '/ticket/<issueIdOrKey>/transition', methods=['POST', 'GET'])
api.add_resource(Attachment, '/ticket/<issueIdOrKey>/attach', methods=['POST'])

#Lime api
api.add_resource(LimePreConvertion, '/lime/setup', methods=['POST'])
api.add_resource(FetchFile, '/lime/get_log_files/<ticket_id>')
