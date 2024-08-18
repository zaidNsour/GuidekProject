from flask import Blueprint, request, jsonify
from app import db
from app.models import College, Major, MajorSubject, Subject
from flask_jwt_extended import jwt_required
from app.decorators import admin_required
from sqlalchemy.exc import SQLAlchemyError

major_bp = Blueprint('majors', __name__, url_prefix='/majors')

@major_bp.route('/add_majors', methods = ['POST'])
#@admin_required
def add_majors():
  try:   
    data = request.get_json()
    for major in data:
      name = major.get('name')
      college_name = major.get('college_name')
      college = College.query.filter_by(name = college_name).first()
      if not college:
        return jsonify({"message": "invalid college name"}), 201
    
      major = Major(name = name, college = college )
      db.session.add(major)
    db.session.commit()

    return jsonify({"message": "majors added successfully"}), 201
  

  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while adding the transaction', 'error': str(e)}), 500
  
    
  except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while adding the transaction', 'error': str(e)}), 500
  
  
@major_bp.route('/all_majors', methods = ['GET'])
def all_subjects():
  try:
    majors = Major.query.all()
    major_list = [major.to_dict() for major in  majors]
    
    return jsonify({"majors": major_list}), 200
  
  except SQLAlchemyError as e:
        return jsonify({'message': 'Database error occurred while get the majors', 'error': str(e)}), 500
  
  except Exception as e:
 
        return jsonify({'message': 'An error occurred while get the majors', 'error': str(e)}), 500


@major_bp.route('/add_subjects_to_majors', methods = ['POST'])
#@admin_required
def add_subjects_to_majors():
  try:   
    data = request.get_json()
    for added_subject in data:

      major_name = added_subject.get('major_name')
      subject_name = added_subject.get('subject_name')
      num_of_hours = added_subject.get('num_of_hours')
      year = added_subject.get('year')
      semester = added_subject.get('semester')

      if not all([major_name, subject_name, year, semester]):
        return jsonify({'message': 'Missing major_name, subject_name, num_of_hours, year, or semester'}), 400


      major = Major.query.filter_by(name = major_name).first()
      if not major:
        return jsonify({"message": "invalid major name"}), 400
      
      subject = Subject.query.filter_by(name = subject_name).first()
      if not subject:
        return jsonify({"message": "invalid subject name"}), 400
      
      if not subject_name:
        return jsonify({'message': 'Missing Subject name.'}), 400
      

      major_subject = MajorSubject(major_id = major.id,
                                  subject_id = subject.id,
                                  num_of_hours = num_of_hours,
                                  year = year,
                                  semester = semester  
                                )
      db.session.add(major_subject)
    db.session.commit()

    return jsonify({"message": "major subjects added successfully"}), 201
  

  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while adding the transaction', 'error': str(e)}), 500
  
    
  except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while adding the transaction', 'error': str(e)}), 500


@major_bp.route('/get_subjectsen/<major_name>', methods = ['GET'])
#@admin_required
def get_subject(major_name):
  try:   
    major = Major.query.filter_by(name = major_name).first()
    if not major:
       return jsonify({"message": "Invalid major name"}), 400
    subjects = MajorSubject.query.filter_by(major_id = major.id).all()
    subjects_list = [subject.to_dict() for subject in  subjects]
    return jsonify({"Subjects": subjects_list}), 200
  

  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred ', 'error': str(e)}), 500
  
    
  except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500