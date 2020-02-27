import json
import requests
from flask import request
from flask_restful import Resource
from requests.auth import HTTPBasicAuth
from werkzeug.exceptions import BadRequest

from app.models.users import Users
import logging

from app.utils.custom_response import make_resp

class UserProfile(Resource):
	def get(self):
		try:
			email = request.args.get('email', type=str)
			user = Users.get_user(email)
			logging.debug("------User--{}---Email---{}---".format(user, email))  
			return make_resp({'user': user}, 200)
		except Exception as inst:
			logging.debug("---Getting failed---inst--{}------".format(inst))
			return make_resp({'status' : 'failure', 'message': 'User Not found' }, 404)

	def post(self):
		params = request.args.to_dict()
		if not params or not 'email' in params or not 'jira_username' in params or 'jira_token' not in  params or not 'git_token' in params or not 'git_username' in params:
			raise BadRequest()
		user = {'email' : request.args['email'],
	  	'jira_username': request.args['jira_username'],
	  	'jira_token': request.args['jira_token'],
	  	'git_username': request.args['git_username'],
	  	'git_token': request.args['git_token']
		}
		try:
			logging.info("------Creating}---")  
			new_user = Users.new_user(user)
			logging.info("------User--{}---Email------".format(new_user))
			logging.debug("------User--{}---Email------".format(new_user))  
			return make_resp({'success' : 'User created successfully!'}, 201)
		except Exception as inst:
			logging.info("------User-creation failed-{}---Email------".format(inst))  
			logging.debug("------User-creation failed-{}---Email------".format(inst)) 
			return make_resp({'failure' : 'failure' }, 500)