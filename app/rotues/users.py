from flask import Blueprint, jsonify
from app.models import User
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/current_user_info', methods=['GET'])
@jwt_required()
def current_user_info():
  email = get_jwt_identity()
  user = User.query.filter_by(email = email).first()

  return jsonify(user.to_dict()), 200  


@user_bp.route('/all_users', methods = ['GET'])
def all_users():
  users = User.query.all()
  users_list = [user.to_dict() for user in users]
  
  return jsonify({"users": users_list}), 200