from flask import Blueprint, request, jsonify
from app import db
from app.decorators import admin_required
from app.models import  QA
from flask_jwt_extended import  jwt_required
from sqlalchemy.exc import SQLAlchemyError


faq_bp = Blueprint('faq', __name__, url_prefix='/faq')

@faq_bp.route('/add_qa', methods = ['POST'])
@admin_required 
def add_qa():
  try:
    data = request.get_json()
    for d in data:
      question = d.get('question')
      answer = d.get('answer')

      qa = QA(question = question, answer = answer)
      db.session.add(qa)
    db.session.commit()

    return jsonify({"message": "QA added successfully"}), 201
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while add QA', 'error': str(e)}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while add QA', 'error': str(e)}), 500


@faq_bp.route('/all_qa', methods = ['GET'])
@jwt_required() 
def all_qa():
  qas = QA.query.all()
  qas_list = [qa.to_dict() for qa in qas]
  
  return jsonify({"QA": qas_list}), 200