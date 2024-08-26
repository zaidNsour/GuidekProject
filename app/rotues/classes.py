from flask import Blueprint, request, jsonify
from app import db
from app.models import  ClassRequest, Subject
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User
from sqlalchemy.exc import SQLAlchemyError


class_bp = Blueprint('classes', __name__, url_prefix='/classes')

@class_bp.route('/request_class', methods = ['POST'])
@jwt_required() 
def request_class():
  try:
    email = get_jwt_identity()
    user = User.query.filter_by(email = email).first()
    data = request.get_json()
    subject_name = data.get('subject_name')

    if not subject_name:
      return jsonify({'message': 'Missing Subject name.'}), 400

    subject = Subject.query.filter_by(name = subject_name).first()
    if not subject:
      return jsonify({'message': 'Invalid Subject name.'}), 400
    
    class_request = ClassRequest.query.filter_by(student_id = user.id, subject_id = subject.id).first()
    if class_request:
      return jsonify({"message": "request already exist."}), 400
    
    class_request = ClassRequest(student_id = user.id, subject_id = subject.id)
    db.session.add(class_request)
    db.session.commit()

    return jsonify({"message": "Class request created successfully."}), 201
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while adding class request', 'error': str(e)}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while adding class request', 'error': str(e)}), 500