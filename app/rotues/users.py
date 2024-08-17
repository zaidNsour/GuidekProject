from flask import Blueprint, flash, jsonify, render_template, request
from app.forms import ResetPasswordForm
from app.models import Major, User
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from app.helper import send_reset_email
from app.validators import validate_email, validate_fullname, validate_phone, validate_number
from app import  db
from werkzeug.security import generate_password_hash
from app.helper import upload_picture, get_picture, delete_picture
import json


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
 
  user = User.query.filter_by(email = email).first()
  if user:
    send_reset_email(user)

  return jsonify({'message': 'If this account exist, you will recieve an email with isntruction'}),200
  
  
@user_bp.route("/reset_password/<token>", methods=['GET','POST'])
def reset_password(token):
  
   user= User.verify_token(token)
   if not user:
      flash('The token is invalid or expired', 'warning')
   
   form = ResetPasswordForm()
   if form.validate_on_submit():
      hashed_password = generate_password_hash(form.password.data)
      user.password = hashed_password
      db.session.commit()
      flash(message="your Password has been updated successfully",category="success")

   return render_template('reset_password.html', title='Reset Password', form = form)


### these routes for test the image upload and retreive

@user_bp.route('/upload_image', methods = ['POST'])
@jwt_required()
def upload_image():
  image_file = request.files['image']
  upload_picture(image_file, 'app/static/images/user-images/', (250,250))
  return jsonify({"message":"Image uploaded successfully."})


@user_bp.route('/get_image/<filename>', methods=['GET'])
@jwt_required()
def get_image(filename):
  try:       
    return get_picture('app/static/images/user-images/', filename)
  except FileNotFoundError:
    return jsonify({"error": "Image not found"}), 404

### these routes for test the image upload and retreive


@user_bp.route("/update_user_info", methods=["PUT"])
@jwt_required()
def update_user_info():
  email = get_jwt_identity()
  user = User.query.filter_by(email = email).first()
  json_data = request.form.get('json_data')
  if json_data:
    data = json.loads(json_data)
  else:
    return jsonify({"error": "No JSON data provided"}), 400
  
  image_file = request.files.get('image')
  fullname = data.get('fullname')
  number = data.get('number')
  phone = data.get('phone')
  major_name = data.get('major_name')

  if image_file:
    picture_name = upload_picture( image_file, 'app/static/images/user-images/', (250,250) ) 
    if picture_name == 'unsupported':
      return jsonify({"error": "Unsupported image type"}), 400
     #modify this after modify data base
    if user.img_url != 'default_image.jpg':
      delete_picture('app/static/images/user-images/', user.img_url)
    user.img_url = picture_name

  if fullname:
    if not validate_fullname(fullname):
      return jsonify({'message': 'Invalid fullname'}), 400
    user.fullname = fullname

  if number:
    if not validate_number(number):
      return jsonify({'message': 'Invalid student number'}), 400
    user.number = number

  if phone:
    if not validate_phone(phone):
      return jsonify({'message': 'Invalid phone number'}), 400
    user.phone = phone

  if major_name:
    major = Major.query.filter_by(name = major_name).first()
    if major:
      user.major = major

  db.session.commit()
  return jsonify({'message': 'User Profile updated successfully.'}), 200


   
   
  


  
    
  










