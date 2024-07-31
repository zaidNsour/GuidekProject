import os
from flask import Blueprint, request, jsonify
from app import db, mail
from app.models import User
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from app.validators import validate_email, validate_password, validate_fullname

from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required
from flask_jwt_extended import get_jwt_identity


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def send_verification_email(email, code):
  msg = Message('Your verification code', sender= os.environ.get('EMAIL_USER'), recipients=[email])
  msg.body = f'Your verification code is {code}'
  mail.send(msg)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
  email = get_jwt_identity()
  new_access_token = create_access_token(identity = email)
  return jsonify(access_token=new_access_token), 200


@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  fullname = data.get('fullname')
  email = data.get('email')
  password = data.get('password')

  if not all([fullname, email, password]):
    return jsonify({'message': 'Missing fullname, email, or password'}), 400
    

  if not validate_fullname(fullname):
    return jsonify({'message': 'Invalid fullname'}), 400

  if not validate_email(email):
    return jsonify({'message': 'Invalid email format'}), 400

  is_valid_password, password_message = validate_password(password)
  if not is_valid_password:
    return jsonify({'message': password_message}), 400


  if User.query.filter_by(email = email).first():
    return jsonify({'message': 'User already exists'}), 400

  hashed_password = generate_password_hash(password)
  user = User(fullname = fullname, email = email, password = hashed_password)
  db.session.add(user)
  db.session.commit()
  #verification_code = random.randint(100000, 999999)
  #send_verification_email(email, verification_code)
  
  return jsonify({'message': 'User registered successfully. Please check your email to activate your account.'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  if not all([email, password]):
    return jsonify({'message': 'Missing email or password'}), 400

  user = User.query.filter_by(email = email).first()

  # if user and not user.verified:
  # 	return jsonify({'message': 'Email not verified'}), 400

  if user and check_password_hash(user.password, password):
    access_token = create_access_token(identity = email)
    refresh_token = create_refresh_token(identity = email)
    return jsonify(access_token = access_token, refresh_token = refresh_token), 200
  else:
    return jsonify({'message': 'Invalid email or password'}), 400
    

# if you want to add email verification endpoint
'''
@auth_bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    user = User.query.filter_by(email=email, verification_code=code).first()

    if not user:
      return jsonify({'message': 'Invalid email or verification code'}), 400

    user.verified = True
    user.verification_code = None
    db.session.commit()

    return jsonify({'message': 'Email verified successfully'}), 200
'''


