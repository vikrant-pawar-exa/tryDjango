from flask import Blueprint
from flask import Flask, request, Response
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest
import requests, json
from requests.auth import HTTPBasicAuth
jira_bp = Blueprint('jira_blueprint', __name__)


api = Api(jira_bp)


class TicketUnresolved(Resource):
    def get(self):
        try:
            assigneeEmail = request.headers.get('email', '')
            if assigneeEmail == '':
                raise BadRequest()
            url = "http://exabeam.atlassian.net/rest/api/3/search?expand=names&maxResults=50&" \
                  "jql=assignee%3D%22{}%22 %26 status not in (Resolved,Closed)".format(assigneeEmail)
            headers = {
                "Accept": "application/json",
            }
            response = requests.request("GET", url, auth=HTTPBasicAuth('akshay.pange@exabeam.com',
                                                                       '08wmmbS7IVY6n9f1pUGiAB04'), headers=headers)
        except BadRequest:
            return {"message": "Please provide valid details(email/name) of assignee"}, 400
        except Exception:
            return {"message":"Internal server error"}, 500
        return parse_response(response)


class Ticket(Resource):
    def get(self):
        try:
            maxResults = request.args.get('maxResults', default=50, type=str)
            assigneeEmail = request.headers.get('email', '')
            if assigneeEmail == '':
                raise BadRequest()
            url = "http://exabeam.atlassian.net/rest/api/2/search?" \
                  "jql=assignee%3D%22{}%22&expand=names&maxResults={}".format(assigneeEmail, maxResults)
            headers = {
                "Accept": "application/json",
            }
            response = requests.request("GET", url, auth=HTTPBasicAuth('akshay.pange@exabeam.com',
                                                                       '08wmmbS7IVY6n9f1pUGiAB04'), headers=headers)
        except BadRequest:
            return {"message": "Please provide valid details(email/name) of assignee"}, 400
        except Exception:
            return {"message": "Internal server error"}, 500
        return parse_response(response)


class Comments(Resource):
    def get(self,issueIdOrKey):
        url = "http://localhost:8080/rest/api/2/issue/{}/comment".format(issueIdOrKey)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.request("GET", url, auth=HTTPBasicAuth('akshaypange738',
                                                                   'Aniket@738'), headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            return response.json(), 200
        else:
            return handle_response(response)

    def post(self,issueIdOrKey):
        url = "http://localhost:8080/rest/api/2/issue/{}/comment".format(issueIdOrKey)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        print(request.data)
        response = requests.request("POST", url, auth=HTTPBasicAuth('akshaypange738',
                                                                    'Aniket@738'), headers=headers,
                                    data=request.data)
        if response.status_code == 201 or response.status_code == 200:
            return response.json(), 201
        else:
            return handle_response(response)


class UpdateComments(Resource):
    def put(self, issueIdOrKey, commentId):
        url = "http://localhost:8080/rest/api/2/issue/{}/comment/{}".format(issueIdOrKey,commentId)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.request("PUT", url, auth=HTTPBasicAuth('akshaypange738',
                                                                   'Aniket@738'), headers=headers,
                                    data=request.data)
        if response.status_code == 201:
            return response.json(), 201
        else:
            return handle_response(response)


class Attachment(Resource):
    def post(self,issueIdOrKey):
        if request.method == "POST":
            url = "http://localhost:8080/rest/api/2/issue/{{issueIdOrKey}}/attachments".replace('{{issueIdOrKey}}',
                                                                                             "10022")
            print(url)
            headers = {
                "Accept": "application/json",
                "Content-Type": "multipart/form-data",
                "X - Atlassian - Token": "nocheck"
            }
            #files = {'file': open(request.files['file'], 'rb')}
            response = requests.post( url, auth=HTTPBasicAuth('akshaypange738',
                                                                        'Aniket@738'), headers=headers, files=request.files)
        if response.status_code == 200:
            return response.json(), 200
        else:
            return handle_response(response)


api.add_resource(TicketUnresolved, '/tickets/unresolve_ticket')
api.add_resource(Ticket, '/tickets', endpoint="tickets")
api.add_resource(Comments, '/comments/<issueIdOrKey>')
api.add_resource(UpdateComments, '/comments/<issueIdOrKey>/<commentId>',methods=['PUT'])
api.add_resource(Attachment, '/attach/<issueIdOrKey>', methods=['POST'])


def parse_response(response):
    if response.status_code == 200:
        response_json = json.loads(response.text)
        content = []
        customfeild_for_sf=''
        issues = response_json['issues']
        if len(issues) != 0:
            names = response_json['names']
            for name, sf_customfield in names.items():
                if sf_customfield == 'Salesforce Customer':
                    customfeild_for_sf = name

        for issue in issues:
            dict = {
                "id": issue['key'],
                "assignee": issue['fields']['assignee']['displayName'],
                "priority": issue['fields']['priority']['name'],
                "status": issue['fields']['status']['name'],
                "summary": issue['fields']['summary'],
                "Salesforce Customer": issue['fields'][customfeild_for_sf]
            }
            content.append(dict)
        return {'issue': content}, 200
    else:
        return handle_response(response)


def handle_response(response):
    if response.status_code == 401:
        return {"message":'authentication credentials are incorrect or missing'}, 401
    elif response.status_code == 403:
        return {"message":'Basic auth with password is not allowed on this instance'}, 403
    elif response.status_code == 404:
        return {"message":'Either issue is not found or the user does not ' \
               'have permission to view it.'}, 404
    else:
        return {"message":'Internal server error'}, 500
