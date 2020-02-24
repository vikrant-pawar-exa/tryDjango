import sys, logging
from flask import jsonify, request
from flask_restful import Resource

from app.utils.file_converter import Triage
from app.utils.custom_response import make_resp

class LimePreConvertion(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return make_resp({'message': 'No input data provided'}, 400)
        ticket_number = json_data["ticketNumber"]
        log_file_path = json_data["logFilePath"]
        return Triage().lime_setup(ticket_number, log_file_path)

class FetchFile(Resource):

    def get(self, ticket_id):
        try:
            return Triage().get_log_files(ticket_id)
        except:
            logging.error("----Exception in Fetch file API : {}".format(sys.exc_info()[1]))
            return make_resp({"message": "Exception in API: {}".format(sys.exc_info()[1])}, 422)
        