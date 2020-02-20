import json
import sys, logging
import requests
from flask import request
from flask_restful import Resource
from requests.auth import HTTPBasicAuth
from werkzeug.exceptions import BadRequest
from app.utils.constant import Constants
from config import Config
from app.utils.custom_response import make_resp


SCHEME = "http://"


class TicketUnresolved(Resource):
    """
    Get unresolved tickets assigned to user
    """
    def get(self):
        """
        Get unresolved issue assigned to user
        :return: json response
        """
        try:
            logging.info('Enter in get TicketUnresolved JIRA api')
            assigneeEmail = request.headers.get('email', '')
            if assigneeEmail == '':
                raise BadRequest()
            url = SCHEME + Config.HOST_JIRA + Constants.UNRESOLVED_TICKET_URL.format(assigneeEmail)
            headers = {
                "Accept": "application/json",
            }
            response = requests.request("GET", url, auth=HTTPBasicAuth(Config.USERNAME_JIRA,
                                                                       Config.PASSWORD_JIRA), headers=headers)
        except BadRequest:
            logging.error("----Exception email/name of assignee not be null : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Please provide valid details(email/name) of assignee"}, 400)
        except :
            logging.error("----Exception in JIRA TicketUnresolved API : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Exception in API: {}".format(sys.exc_info()[1])}, 422)
        logging.info("Exit from TicketUnresolved ")
        return parse_response(response)


class Ticket(Resource):
    def get(self):
        """
         Get issues assigned to user
         :return: json response
         """
        logging.info('Enter in get Ticket JIRA api')
        try:
            maxResults = request.args.get('maxResults', default=50, type=str)
            assigneeEmail = request.headers.get('email', '')
            if assigneeEmail == '':
                raise BadRequest()
            url = SCHEME + Config.HOST_JIRA+ Constants.GET_TICKET_URL.format(assigneeEmail, maxResults)
            headers = {
                "Accept": "application/json",
            }
            response = requests.request("GET", url, auth=HTTPBasicAuth(Config.USERNAME_JIRA,
                                                                       Config.PASSWORD_JIRA), headers=headers)
        except BadRequest:
            logging.error("----Exception email/name of assignee not be null : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Please provide valid details(email/name) of assignee"}, 400)

        except:
            logging.error("----Exception in JIRA Ticket API : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Exception in API: {}".format(sys.exc_info()[1])}, 422)
        logging.info("Exit from Ticket ")
        return parse_response(response)


class Comments(Resource):
    """
    Get and add comment for an issue
    """
    def get(self,issueIdOrKey):
        """
         Get comments of particular issue
         :return: json response
        """
        logging.info('Enter in get Comments JIRA api')
        try:
            url = SCHEME + Config.HOST_JIRA + Constants.GET_COMMENTS_URL.format(issueIdOrKey)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            response = requests.request("GET", url, auth=HTTPBasicAuth(Config.USERNAME_JIRA,
                                                                       Config.PASSWORD_JIRA), headers=headers)
            if response.status_code == 200 or response.status_code == 201:
                return response.json(), 200
            else:
                return handle_response(response)
        except:
            logging.error("----Exception in JIRA TicketUnresolved API : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Exception in API: {}".format(sys.exc_info()[1])}, 422)

    def post(self,issueIdOrKey):
        """
          post comments for particular issue
          :return: json response
        """
        logging.info('Enter in post Comments JIRA api')
        try:
            url = SCHEME + Config.HOST_JIRA + Constants.GET_COMMENTS_URL.format(issueIdOrKey)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            response = requests.request("POST", url, auth=HTTPBasicAuth(Config.USERNAME_JIRA,
                                                                        Config.PASSWORD_JIRA), headers=headers,
                                        data=request.data)
            if response.status_code == 201 or response.status_code == 200:
                return response.json(), 200
            else:
                return handle_response(response)
        except:
            logging.error("----Exception in JIRA Comments post API : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Exception in API: {}".format(sys.exc_info()[1])}, 422)



class UpdateComments(Resource):
    def put(self, issueIdOrKey, commentId):
        """
          Update comments for particular issue
          :return: json response
        """
        try:
            logging.info('Enter in UpdateComments JIRA api')
            url = SCHEME + Config.HOST_JIRA + Constants.UPDATE_COMMENT_URL.format(issueIdOrKey, commentId)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            response = requests.request("PUT", url, auth=HTTPBasicAuth(Config.USERNAME_JIRA,
                                                                       Config.PASSWORD_JIRA), headers=headers,
                                        data=request.data)
            if response.status_code == 200:
                return response.json(), 200
            else:
                return handle_response(response)
        except:
            logging.error("----Exception in JIRA UpdateComments  API : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Exception in API: {}".format(sys.exc_info()[1])}, 422)


class Transition(Resource):
    def post(self, issueIdOrKey):
        """
          change status for particular issue
          :return: json response
        """
        logging.info('Enter in Transition JIRA api')
        try:
            status = request.args.get('status', '')
            print(status)
            if status == '':
                raise BadRequest
            url = SCHEME + 'localhost:8080' + '/rest/api/2/issue/{}/transitions'.format(issueIdOrKey)
            print(url)
            headers = {

                "Content-Type": "application/json"
            }
            response = requests.request("GET", url, auth=HTTPBasicAuth(Config.USERNAME_JIRA,
                                                                       Config.PASSWORD_JIRA), headers=headers)
            if response.status_code == 200:
                response_json = json.loads(response.text)
                transitions = response_json['transitions']
                for transition in transitions:
                    if str(transition["name"]) == str(status):
                        transition_id = transition['id']
                        data = {"transition": {"id": transition_id}}
                        post_response = requests.request("POST", url, auth=HTTPBasicAuth(Config.USERNAME_JIRA,
                                                                                         Config.PASSWORD_JIRA), headers=headers,
                                                         data=json.dumps(data))
                        if post_response.status_code == 204:
                            return make_resp({"message": "Status successfully updated"}, 200)
                        else:
                            handle_response(post_response)
                return make_resp({"message": "transition not possible"}, 500)
            else:
                return handle_response(response)
        except:
            logging.error("----Exception in JIRA Transition API : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Exception in API: {}".format(sys.exc_info()[1])}, 422)


class Attachment(Resource):
    def post(self,issueIdOrKey):
        """
          Add Attachment for particular issue
          :return: json response
          """
        logging.info('Enter in Attachment JIRA api')
        if request.method == "POST":
            url = SCHEME + Config.HOST_JIRA+ Constants.ADD_ATTACHMENT_URL.format(issueIdOrKey)
            headers = {
                "Accept": "application/json",
                "Content-Type": "multipart/form-data",
                "X - Atlassian - Token": "nocheck"
            }
            response = requests.post(url, auth=HTTPBasicAuth(Config.USERNAME_JIRA,
                                                             Config.PASSWORD_JIRA), headers=headers, files=request.files)
        if response.status_code == 200:
            return response.json(), 200
        else:
            return handle_response(response)


def parse_response(response):
    """
      Parse the response in appropriate format
      :return: json response
    """
    logging.info('Enter in parse_response JIRA api')
    try:
        if response.status_code == 200:
            response_json = json.loads(response.text)
            content = []
            custom_field_for_sf = None
            issues = response_json['issues']
            if len(issues) != 0:
                names = response_json['names']
                for name, sf_custom_field in names.items():
                    if sf_custom_field == 'Salesforce Customer':
                        custom_field_for_sf = name
            if custom_field_for_sf != None:
                for issue in issues:
                    dict = {
                        "id": issue['key'],
                        "assignee": issue['fields']['assignee']['displayName'],
                        "priority": issue['fields']['priority']['name'],
                        "status": issue['fields']['status']['name'],
                        "summary": issue['fields']['summary'],
                        "Salesforce Customer": issue['fields'][custom_field_for_sf]
                    }
                    content.append(dict)
            else:
                return make_resp({"message": "Exception in API:Parsing error Custom_feild for"
                                             " Salesforce Customer not found"}, 422)
            return {'issue': content}, 200
        else:
            return handle_response(response)
    except:
        logging.error("----Exception in JIRA parse_response API ")
        return make_resp({"message": "Exception in API: Parsing error"}, 422)


def handle_response(response):
    """
      Handel the response
      :return: message with status code
      """
    logging.info('Enter in handle_response JIRA api')
    if response.status_code == 401:
        return make_resp({"message":'authentication credentials are incorrect or missing'}, 401)
    elif response.status_code == 403:
        return make_resp({"message":'Basic auth with password is not allowed on this instance'}, 403)
    elif response.status_code == 404:
        return make_resp({"message":'Either issue is not found or the user does not ' \
               'have permission to view it.'}, 404)
    else:
        return make_resp({"message":'Internal server error'}, 500)