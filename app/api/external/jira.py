import json
import requests
from flask import request
from flask_restful import Resource
from requests.auth import HTTPBasicAuth
from werkzeug.exceptions import BadRequest
from app.utils.constant import Constants
from config import Config


SCHEME = "http://"


class TicketUnresolved(Resource):
    """
    Get unresolved tickets assigned to user
    """
    def get(self):
        """
        Get unresolved issue assigned to user
        :return: dictionary of issue
        """
        try:
            assigneeEmail = request.headers.get('email', '')
            if assigneeEmail == '':
                raise BadRequest()
            url = SCHEME + Config.HOST_GIT + Constants.UNRESOLVED_TICKET_URL.format(assigneeEmail)
            headers = {
                "Accept": "application/json",
            }
            response = requests.request("GET", url, auth=HTTPBasicAuth(Config.USERNAME_GIT,
                                                                       Config.PASSWORD_GIT), headers=headers)
        except BadRequest:
            return {"message": "Please provide valid details(email/name) of assignee"}, 400
        except Exception:
            return {"message":"Internal server error"}, 500
        return parse_response(response)


class Ticket(Resource):
    def get(self):
        """
         Get issues assigned to user
         :return: dictionary of issue
         """
        try:
            maxResults = request.args.get('maxResults', default=50, type=str)
            assigneeEmail = request.headers.get('email', '')
            if assigneeEmail == '':
                raise BadRequest()
            url = SCHEME + Config.HOST_GIT + Constants.GET_TICKET_URL.format(assigneeEmail, maxResults)
            headers = {
                "Accept": "application/json",
            }
            response = requests.request("GET", url, auth=HTTPBasicAuth(Config.USERNAME_GIT,
                                                                       Config.PASSWORD_GIT), headers=headers)
        except BadRequest:
            return {"message": "Please provide valid details(email/name) of assignee"}, 400
        except Exception:
            return {"message": "Internal server error"}, 500
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
        url = SCHEME + Config.HOST_GIT + Constants.GET_COMMENTS_URL.format(issueIdOrKey)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.request("GET", url, auth=HTTPBasicAuth(Config.USERNAME_GIT,
                                                                   Config.PASSWORD_GIT), headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            return response.json(), 200
        else:
            return handle_response(response)

    def post(self,issueIdOrKey):
        """
          post comments for particular issue
          :return: json response
        """
        url = SCHEME + Config.HOST_GIT + Constants.GET_COMMENTS_URL.format(issueIdOrKey)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        print(request.data)
        response = requests.request("POST", url, auth=HTTPBasicAuth(Config.USERNAME_GIT,
                                                                    Config.PASSWORD_GIT), headers=headers,
                                    data=request.data)
        if response.status_code == 201 or response.status_code == 200:
            return response.json(), 201
        else:
            return handle_response(response)


class UpdateComments(Resource):
    def put(self, issueIdOrKey, commentId):
        """
          Update comments for particular issue
          :return: json response
          """
        url = SCHEME + Config.HOST_GIT + Constants.UPDATE_COMMENT_URL.format(issueIdOrKey, commentId)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.request("PUT", url, auth=HTTPBasicAuth(Config.USERNAME_GIT,
                                                                   Config.PASSWORD_GIT), headers=headers,
                                    data=request.data)
        if response.status_code == 200:
            return response.json(), 200
        else:
            return handle_response(response)


class Attachment(Resource):
    def post(self,issueIdOrKey):
        """
          Add Attachment for particular issue
          :return: json response
          """
        if request.method == "POST":
            url = SCHEME + Config.HOST_GIT + Constants.ADD_ATTACHMENT_URL.format(issueIdOrKey)
            headers = {
                "Accept": "application/json",
                "Content-Type": "multipart/form-data",
                "X - Atlassian - Token": "nocheck"
            }
            response = requests.post(url, auth=HTTPBasicAuth(Config.USERNAME_GIT,
                                                             Config.PASSWORD_GIT), headers=headers, files=request.files)
        if response.status_code == 200:
            return response.json(), 200
        else:
            return handle_response(response)


def parse_response(response):
    """
      Parse the response in appropriate format
      :return: json response
    """
    if response.status_code == 200:
        response_json = json.loads(response.text)
        content = []
        custom_field_for_sf =''
        issues = response_json['issues']
        if len(issues) != 0:
            names = response_json['names']
            for name, sf_custom_field in names.items():
                if sf_custom_field == 'Salesforce Customer':
                    custom_field_for_sf = name

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
        return {'issue': content}, 200
    else:
        return handle_response(response)


def handle_response(response):
    """
      Handel the response
      :return: message with status code
      """
    if response.status_code == 401:
        return {"message":'authentication credentials are incorrect or missing'}, 401
    elif response.status_code == 403:
        return {"message":'Basic auth with password is not allowed on this instance'}, 403
    elif response.status_code == 404:
        return {"message":'Either issue is not found or the user does not ' \
               'have permission to view it.'}, 404
    else:
        return {"message":'Internal server error'}, 500