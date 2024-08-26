from flask import Blueprint, request, jsonify
from app import db
from app.models import College, Major
from flask_jwt_extended import jwt_required
from app.decorators import admin_required
from sqlalchemy.exc import SQLAlchemyError

college_bp = Blueprint('colleges', __name__, url_prefix='/colleges')

@college_bp.route('/add_colleges', methods = ['POST'])
@admin_required
def add_colleges():
  try:   
    data = request.get_json()
    for college in data:
      name = college.get('name')
      location = college.get('location')
    
      college = College(name = name, location = location )
      db.session.add(college)
    db.session.commit()

    return jsonify({"message": "colleges added successfully"}), 201
  
  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while adding the colleges', 'error': str(e)}), 500
  
  except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while adding the colleges', 'error': str(e)}), 500
  