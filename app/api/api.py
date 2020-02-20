from flask import Blueprint, request, jsonify
from flask import Blueprint
from app.utils.custom_response import make_resp
from flask_restful import reqparse, abort, Api, Resource

from app.api.external.jira import *
from app.test_cases.sbt import sbt_resource
from app.models.users import Users

main_api_blueprint = Blueprint('main_api_blueprint', __name__)


@main_api_blueprint.route('/user')
def user_by_email():
	email = request.args.get('email')
	try:
		user = Users.get_user(email)
		return jsonify({'user': user}), 200
	except Exception as inst:
		return jsonify({'status' : 'failure', 'message': 'User Not found' }), 404


@main_api_blueprint.route('/users',methods=['POST'])
def create():
	params = request.args.to_dict()
	if not params or not 'email' in params or not 'jira_username' in params or 'jira_token' not in  params or not 'git_token' in params:
		abort(400)
	user = {'email' : request.args['email'],
  	'jira_username': request.args['jira_username'],
  	'jira_token': request.args['jira_token'],
  	'git_username': request.args['git_username'],
  	'git_token': request.args['git_token']
	}
	try:
		Users.new_user(user)
		return jsonify({'status' : 'success'}), 201
	except Exception as inst:
		return jsonify({'status' : 'failure' }), 500


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

