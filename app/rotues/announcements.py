from flask import Blueprint, request, jsonify
from app import db
from app.models import Announcement
from app.validators import validate_announ_title, validate_announ_content
from app import jwt
from flask_jwt_extended import jwt_required
from app.models import User
from app.decorators import admin_required


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return User.query.filter_by(email = identity).one_or_none()


announ_bp = Blueprint('announcements', __name__, url_prefix='/announcements')


@announ_bp.route('/add_announcement', methods = ['POST'])
@admin_required
@jwt_required() 
def add_announcement():
  data = request.get_json()
  title = data.get('title')
  content = data.get('content')

  if not validate_announ_title(title):
    return jsonify({'message': 'Invalid title'}), 400

  if not validate_announ_content(content):
      return jsonify({'message': 'Invalid content'}), 400
  
  announcement = Announcement(title = title, content = content)
  db.session.add(announcement)
  db.session.commit()

  return jsonify({"message": "Announcement added successfully"}), 201


@announ_bp.route('/all_announcements', methods = ['GET'])
def get_announcement():
  announcements = Announcement.query.all()
  announcement_list = [announcement.to_dict() for announcement in announcements]
  
  return jsonify({"announcements": announcement_list}), 200

