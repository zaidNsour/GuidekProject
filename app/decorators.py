from flask import jsonify
from functools import wraps
from flask_jwt_extended import jwt_required,current_user



def admin_required(fn):
  @wraps(fn)
  @jwt_required()
  def wrapper(*args, **kwargs):
    user = current_user
    if not user or not user.is_admin:
      print(f"Current User: {user}")
      return jsonify({"message": "Admin access required"}), 403
    return fn(*args, **kwargs)
  return wrapper