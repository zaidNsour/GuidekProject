from flask import Blueprint, request, jsonify
from app import db
from app.models import Major
from flask_jwt_extended import jwt_required
from app.decorators import admin_required

major_bp = Blueprint('majors', __name__, url_prefix='/majors')

@major_bp.route('/add_majors', methods = ['POST'])
@admin_required
@jwt_required() 
def add_majors():
 data = request.get_json()
 for major in data:
  name = major.get('name')
  college_id = major.get('college_id')
 

  major = Major(name = name, college_id = college_id )
  db.session.add(major)
 db.session.commit()

 return jsonify({"message": "majors added successfully"}), 201