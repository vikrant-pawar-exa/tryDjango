from flask import jsonify, request
from flask_restful import Resource
from app.utils.lime_file_converter import LimeConverter

class Lime(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return make_resp({'message': 'No input data provided'}, 400)
        ticket_number = json_data["ticketNumber"]
        log_file_path = json_data["logFilePath"]
        return LimeConverter().lime_setup(ticket_number, log_file_path)