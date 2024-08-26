from flask import Blueprint, request, jsonify
from app import db
from app.models import Major, MajorSubject, Subject
from flask_jwt_extended import jwt_required
from app.decorators import admin_required
from sqlalchemy.exc import SQLAlchemyError


subject_bp = Blueprint('subjects', __name__, url_prefix='/subjects')


@subject_bp.route('/add_subjects', methods = ['POST'])
@admin_required
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
@jwt_required()
def all_subjects():
  subjects = Subject.query.all()
  Subject_list = [subject.to_dict() for subject in  subjects]
  
  return jsonify({"subjects": Subject_list}), 200


@subject_bp.route('/subject_resources/<subject_name>', methods = ['GET'])
@jwt_required()
def subject_resources(subject_name):
  try:
    subject = Subject.query.filter_by(name = subject_name).first()
    if not subject:
      return jsonify({'message': 'Invalid Subject name'}), 400
    return jsonify({"subject_resources":
                    {"book":subject.book,
                    "slides":subject.slides,
                    "course_plan":subject.course_plan
                    }}), 200
  
  except SQLAlchemyError as e:
        return jsonify({'message': 'Database error occurred while retrieving the resources', 'error': str(e)}), 500
   
  except Exception as e:
        return jsonify({'message': 'An error occurred while retrieving the resources', 'error': str(e)}), 500

    

@subject_bp.route('/suggested_subjects', methods=['GET'])
def get_suggested_subjects():
  try:
    major_name = request.args.get('major_name')
    year = request.args.get('year')
    semester = request.args.get('semester')

    major = Major.query.filter_by(name = major_name).first()
    if not major:
      return jsonify({'message': 'Invalid Major name'}), 400
      
    subjects_name = []
    major_subjects = MajorSubject.query.filter_by(major_id = major.id, year = year, semester = semester).all()
    for major_subject in major_subjects:
      subject_id =  major_subject.subject_id
      subject = Subject.query.filter_by(id = subject_id).first()
      subjects_name.append(subject.name)

    return jsonify({"suggested_subjects":subjects_name})
  
  except SQLAlchemyError as e:
        return jsonify({'message': 'Database error occurred while retrieving the suggested_subjects', 'error': str(e)}), 500
   
  except Exception as e:
        return jsonify({'message': 'An error occurred while retrieving the suggested_subjects', 'error': str(e)}), 500