from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Major, User, TokenBlocklist
from werkzeug.security import generate_password_hash, check_password_hash
from app.validators import validate_email, validate_number, validate_password, validate_fullname
from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required
from flask_jwt_extended import get_jwt_identity, get_jwt
from app.helper import send_verification_email
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
  try:
    data = request.get_json()
    fullname = data.get('fullname')
    number = data.get('number')
    major_name = data.get('major_name')
    email = data.get('email')
    password = data.get('password')

    if not all([fullname, email, password, number, major_name]):
      return jsonify({'message': 'Missing fullname, email, or password'}), 400
      

    if not validate_fullname(fullname):
      return jsonify({'message': 'Invalid fullname'}), 400

    if not validate_email(email):
      return jsonify({'message': 'Invalid email format'}), 400

    is_valid_password, password_message = validate_password(password)
    if not is_valid_password:
      return jsonify({'message': password_message}), 400
    
    if not validate_number(number):
        return jsonify({'message': 'Invalid student number'}), 400
    
    major = Major.query.filter_by(name = major_name).first()
    if not major:
      return jsonify({'message': 'Invalid major name'}), 400


    if User.query.filter_by(email = email).first():
      return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    user = User(fullname= fullname, email= email, password= hashed_password, number= number, major= major )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully. Please check your email to activate your account.'}), 201
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while register the account', 'error': str(e)}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while register the account', 'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
  try:
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
      return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email = email).first()

    if user and not user.verified:
      return jsonify({'message': 'Email not verified'}), 400

    if user and check_password_hash(user.password, password):
      access_token = create_access_token(identity = email)
      refresh_token = create_refresh_token(identity = email)
      return jsonify(access_token = access_token, refresh_token = refresh_token), 200
    else:
      return jsonify({'message': 'Invalid email or password'}), 400
    
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while login the account', 'error': str(e)}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while login the account', 'error': str(e)}), 500
    

@auth_bp.route('/logout', methods=['GET'])
@jwt_required(verify_type = False) 
def logout():
  try:
    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt['type']
    expires_in = jwt['exp'] - datetime.now().timestamp()

    token_blocked = TokenBlocklist(jti = jti, expires_in = expires_in)
    db.session.add(token_blocked)
    db.session.commit()

    return jsonify({'message': f'{token_type} token is revoked successfully.'}), 200
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while logout the account', 'error': str(e)}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while logout the account', 'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh = True)
def refresh():
  email = get_jwt_identity()
  new_access_token = create_access_token(identity = email)
  return jsonify(access_token=new_access_token), 200


# create end point for verify account request not embedded it in register account 
# because if send_verification_email failed enable user to try again 
@auth_bp.route("/verify_account_request", methods=['POST'])
def verify_request():
  data = request.get_json()
  email = data.get('email')
  if not validate_email(email):
    return jsonify({'message': 'Invalid email format'}), 400
  
  user = User.query.filter_by(email= email).first()
  if user:
    send_verification_email(user)

  return jsonify({'message': 'Check you email for verify your account'}),200


@auth_bp.route('/verify/<token>', methods=['GET'])
def verify(token):
    user= User.verify_token(token)

    if not user:
      return render_template('verified_failed.html', title="Verify Account")

    user.verified = True
    db.session.commit()

    return render_template('verified_success.html', title="Verify Account")



