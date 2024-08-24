from flask import Blueprint, request, jsonify
from app import db
from app.models import Room, College
from flask_jwt_extended import jwt_required
from app.decorators import admin_required
from sqlalchemy.exc import SQLAlchemyError

room_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@room_bp.route('/add_rooms', methods = ['POST'])
#@admin_required 
def add_rooms():
  try:
    data = request.get_json()
    for room in data:
      name = room.get('name')
      college_name= room.get('college_name')
      direction = room.get('direction')

      
      if not all([name, college_name, direction]):
        return jsonify({'message': 'Missing name, college_name, or direction'}), 400

      college = College.query.filter_by(name = college_name).first()
      if not college:
        return jsonify({"message": "college does not exist"}), 400
      
      room = Room(name = name, college = college, direction = direction )
      db.session.add(room)
    db.session.commit()

    return jsonify({"message": "rooms added successfully"}), 201
  
  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while adding the rooms', 'error': str(e)}), 500
  
    
  except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while adding the rooms', 'error': str(e)}), 500



@room_bp.route('/all_rooms', methods = ['GET'])
@jwt_required() 
def all_rooms():
  rooms = Room.query.all()
  rooms_list = [room.to_dict() for room in rooms]
  return jsonify({"rooms": rooms_list}), 200


@room_bp.route('/get_location/<room_name>', methods=['GET'])
@jwt_required()
def get_location(room_name): 
    if not room_name:
        return jsonify({"error": "Room name is required"}), 400
    room = Room.query.filter_by(name = room_name).first()

    if not room:
        return jsonify({"error": "Room not found"}), 404

   
    college = College.query.get(room.college_id)

    if not college:
        return jsonify({"error": "College not found"}), 404

    response = {
        "location": college.location,
        "direction": room.direction
    }

    return jsonify(response)

