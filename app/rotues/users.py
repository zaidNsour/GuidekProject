from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from app.forms import ResetPasswordForm
from app.models import User
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from app.helper import send_reset_email
from app.validators import validate_email
from app import  db
from werkzeug.security import generate_password_hash

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



@user_bp.route("/reset_password_request", methods=['POST'])
def reset_request():
  data = request.get_json()
  email = data.get('email')

  if not validate_email(email):
    return jsonify({'message': 'Invalid email format'}), 400
 
  user = User.query.filter_by(email= email).first()
  if user:
    send_reset_email(user)

  return jsonify({'message': 'If this account exist, you will recieve an email with isntruction'}),201
  
  

@user_bp.route("/reset_password/<token>", methods=['GET','POST'])
def reset_password(token):
  
   user= User.verify_reset_token(token)
   if not user:
      flash('The token is invalid or expired', 'warning')
   
   form= ResetPasswordForm()
   if form.validate_on_submit():
      hashed_password = generate_password_hash(form.password.data)
      user.password = hashed_password
      db.session.commit()
      flash(message="your Password has been updated successfully",category="success")
       
      
   return render_template('reset_password.html', title='Reset Password', form = form)






