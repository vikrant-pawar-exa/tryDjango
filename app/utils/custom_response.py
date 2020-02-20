from flask import jsonify, make_response

def make_resp(message=None, status_code=None):
  response = make_response(jsonify(message), status_code)
  # response.headers["X-success"] = "test"
  return response
