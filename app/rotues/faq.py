from flask import Blueprint, request, jsonify
from app import db
from app.decorators import admin_required
from app.models import  QA, ClassRequest, Subject
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User



faq_bp = Blueprint('faq', __name__, url_prefix='/faq')

@faq_bp.route('/add_qa', methods = ['POST'])
@admin_required
@jwt_required() 
def add_qa():
  data = request.get_json()
  for d in data:
    question = d.get('question')
    answer = d.get('answer')

    qa = QA(question = question, answer = answer)
    db.session.add(qa)
  db.session.commit()

  return jsonify({"message": "QA added successfully"}), 201


@faq_bp.route('/all_qa', methods = ['GET'])
@jwt_required() 
def all_qa():
  qas = QA.query.all()
  qas_list = [qa.to_dict() for qa in qas]
  
  return jsonify({"QA": qas_list}), 200