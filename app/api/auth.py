from flask import Blueprint
from app.utils.custom_response import make_resp


auth_bp = Blueprint('auth_blueprint', __name__)

@auth_bp.route('/login')
def login():
  return make_resp({"message":"Auth api working"})

