from flask import Blueprint, request, jsonify
from app import db
from app.models import Room, College
from flask_jwt_extended import jwt_required
from app.decorators import admin_required

room_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@room_bp.route('/add_rooms', methods = ['POST'])
@admin_required
@jwt_required() 
def add_rooms():
 data = request.get_json()
 for room in data:
  name = room.get('name')
  college_id = room.get('college_id')
  direction = room.get('direction')
 

  room = Room(name = name, college_id = college_id, direction = direction )
  db.session.add(room)
 db.session.commit()

 return jsonify({"message": "rooms added successfully"}), 201


@room_bp.route('/get_location', methods=['GET'])
@jwt_required()
def get_location():
    room_name = request.args.get('name')  

    if not room_name:
        return jsonify({"error": "Room name is required"}), 400


    room = Room.query.filter_by(name=room_name).first()

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

