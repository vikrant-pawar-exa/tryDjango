from flask import Blueprint

auth_bp = Blueprint('auth_blueprint', __name__)

@auth_bp.route('/login')
def login():
  return "This is a AUTH api"