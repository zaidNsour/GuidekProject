from flask import Blueprint, request, jsonify
from app import db
from app.models import College, Subject
from flask_jwt_extended import jwt_required
from app.decorators import admin_required
from sqlalchemy.exc import SQLAlchemyError


subject_bp = Blueprint('subjects', __name__, url_prefix='/subjects')


@subject_bp.route('/add_subjects', methods = ['POST'])
#@admin_required
def add_subjects():
  try:
    data = request.get_json()
    for subject in data:
      name = subject.get('name')
      if not name:
        return jsonify({'message': 'Missing subject name'}), 400
      subject = Subject(name = name)
      db.session.add(subject)
    db.session.commit()
    return jsonify({"message": "Subject added successfully"}), 201
  
  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while adding the subject', 'error': str(e)}), 500
  
    
  except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while adding the subject', 'error': str(e)}), 500



@subject_bp.route('/add_subject', methods = ['POST'])
@admin_required
def add_subject():
  data = request.get_json()
  name = data.get('name')
  num_of_hours = data.get('num_of_hours')
  if not name:
     return jsonify({'message': 'Missing subject name'}), 400

  subject = Subject(name = name, num_of_hours = num_of_hours)
  db.session.add(subject)
  db.session.commit()

  return jsonify({"message": "Subject added successfully"}), 201



@subject_bp.route('/all_subjects', methods = ['GET'])
def all_subjects():
  subjects = Subject.query.all()
  Subject_list = [subject.to_dict() for subject in  subjects]
  
  return jsonify({"subjects": Subject_list}), 200