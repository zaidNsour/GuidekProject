from flask import Blueprint, request, jsonify
from app import db
from app.models import Subject
from flask_jwt_extended import jwt_required
from app.decorators import admin_required


subject_bp = Blueprint('subjects', __name__, url_prefix='/subjects')

@subject_bp.route('/add_subject', methods = ['POST'])
@admin_required
@jwt_required() 
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
  Subject_list = [Subject.to_dict() for Subject in  subjects]
  
  return jsonify({"subjects": Subject_list}), 200