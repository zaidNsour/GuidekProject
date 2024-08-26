import json
from flask import Blueprint, request, jsonify
from app import db
from app.helper import get_picture, upload_picture
from app.models import Announcement
from app.validators import validate_announ_title, validate_announ_content
from app import jwt
from flask_jwt_extended import jwt_required
from app.models import User
from app.decorators import admin_required
from sqlalchemy.exc import SQLAlchemyError


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return User.query.filter_by(email = identity).one_or_none()


announ_bp = Blueprint('announcements', __name__, url_prefix='/announcements')


@announ_bp.route('/add_announcement', methods = ['POST'])
@admin_required
def add_announcement():
  try:
    json_data = request.form.get('json_data')
    if json_data:
      data = json.loads(json_data)
    else:
      return jsonify({"error": "No JSON data provided"}), 400
    
    title = data.get('title')
    content = data.get('content')
    image_file = request.files.get('image')

    if not validate_announ_title(title):
      return jsonify({'message': 'Invalid title'}), 400
    
    if not validate_announ_content(content):
        return jsonify({'message': 'Invalid content'}), 400
    
    announcement = Announcement(title = title, content = content)

    if image_file:
      picture_name = upload_picture( image_file, 'app/static/images/announ-images/', (300,300) ) 
      if picture_name == 'unsupported':
        return jsonify({"error": "Unsupported image type"}), 400
      
      announcement.img_url = picture_name
  
    db.session.add(announcement)
    db.session.commit()
    return jsonify({"message": "Announcement added successfully"}), 201
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while adding the announcement', 'error': str(e)}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while adding the announcement', 'error': str(e)}), 500
  


@announ_bp.route('/get_image/<filename>', methods=['GET'])
@jwt_required()
def get_image(filename):
  try:       
    return get_picture('app/static/images/announ-images/', filename)
  except FileNotFoundError:
    return jsonify({"error": "Image not found"}), 404
  

@announ_bp.route('/all_images_name', methods = ['GET'])
@jwt_required()
def all_image_name():
  try:
    announcements = Announcement.query.all()
    images_info = [{"image_name":announcement.to_dict().get("img_url"), "id":announcement.to_dict().get("id")} 
                   for announcement in announcements]
 
    return jsonify({"images_info": images_info}), 200
  
  
  except SQLAlchemyError as e:
    return jsonify({'message': 'Database error occurred while adding the announcement', 'error': str(e)}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while retrieving the announcement', 'error': str(e)}), 500



@announ_bp.route('/all_announcements', methods = ['GET'])
@jwt_required()
def get_announcement():
  try:
    announcements = Announcement.query.all()
    announcement_list = [announcement.to_dict() for announcement in announcements]
    return jsonify({"announcements": announcement_list}), 200
  
  except SQLAlchemyError as e:
    return jsonify({'message': 'Database error occurred while adding the announcement', 'error': str(e)}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while retrieving the announcement', 'error': str(e)}), 500
