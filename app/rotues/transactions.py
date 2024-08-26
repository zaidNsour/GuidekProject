from flask import Blueprint, request, jsonify
from app import db
from app.models import Transaction, TransactionStep
from flask_jwt_extended import jwt_required
from app.decorators import admin_required
from app.validators import validate_expected_time, validate_fee, validate_step_description
from sqlalchemy.exc import SQLAlchemyError

transaction_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transaction_bp.route('/add_transactions', methods = ['POST'])
@admin_required 
def add_transactions():
  try:
    data = request.get_json()
    for transaction in data:
      name = transaction.get('name')
      fee = transaction.get('fee')
      expected_time = transaction.get('expected_time')
      steps_description = transaction.get('steps_description')

      if not all([name, expected_time, steps_description]) and fee != None:
        return jsonify({'message': 'Missing name, fee, expected time, or steps'}), 400
    
      if not validate_fee(fee):
        return jsonify({'message': 'Invalid fee: Must be a float between 0 and 1000'}), 400
    
      if not validate_expected_time(expected_time):
        return jsonify({ 'message': 'Invalid expected time: Must be an integer between 0 and 180'}), 400
      
      if not isinstance(steps_description, list) or not all(validate_step_description(desc) for desc in steps_description):
        return jsonify({'message': 'Invalid step descriptions: Each must be at least 8 characters long'}), 400
    
      transaction = Transaction(name= name, fee= fee,  expected_time= expected_time )

      for index, description in enumerate(steps_description):
        step = TransactionStep(transaction= transaction, number= index + 1, description = description)
        db.session.add(step)

      db.session.add(transaction)

    db.session.commit()

    return jsonify({"message": "Transaction added successfully"}), 201
  
  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while adding the transaction', 'error': str(e)}), 500
  
  except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while adding the transaction', 'error': str(e)}), 500
  


@transaction_bp.route('/add_transaction', methods = ['POST'])
@admin_required 
def add_transaction():
  try:
    data = request.get_json()
    name = data.get('name')
    fee = data.get('fee')
    expected_time = data.get('expected_time')
    steps_description = data.get('steps_description')

    if not all([name, expected_time, steps_description]) and fee != None:
      return jsonify({'message': 'Missing name, fee, expected time, or steps'}), 400
  
    if not validate_fee(fee):
      return jsonify({'message': 'Invalid fee: Must be a float between 0 and 1000'}), 400
  
    if not validate_expected_time(expected_time):
      return jsonify({ 'message': 'Invalid expected time: Must be an integer between 0 and 180'}), 400
    
    if not isinstance(steps_description, list) or not all(validate_step_description(desc) for desc in steps_description):
      return jsonify({'message': 'Invalid step descriptions: Each must be at least 8 characters long'}), 400
  
    transaction = Transaction(name= name, fee= fee,  expected_time= expected_time )
  

    for index, description in enumerate(steps_description):
      step = TransactionStep(transaction= transaction, number= index + 1, description = description)
      db.session.add(step)

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully"}), 201
  
  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while adding the transaction', 'error': str(e)}), 500
  
  except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while adding the transaction', 'error': str(e)}), 500
  


@transaction_bp.route('/all_transactions', methods = ['GET'])
@jwt_required() 
def transactions():
  try:
    transactions = Transaction.query.all()
    transactions_list = [transaction.to_dict() for transaction in  transactions]
    return jsonify({"Transactions": transactions_list}), 200
   
  except SQLAlchemyError as e:
    return jsonify({'message': 'Database error occurred while fetch the transaction', 'error': str(e)}), 500
  
    
  except Exception as e:
    return jsonify({'message': 'An error occurred while fetch the transaction', 'error': str(e)}), 500
  

@transaction_bp.route('/transaction_steps/<string:transaction_name>', methods=['GET'])
@jwt_required() 
def transaction_steps(transaction_name):
  try:
    transaction = Transaction.query.filter_by(name= transaction_name).first()
    if not transaction:
      return jsonify({'message': 'Invalid transaction name'}), 404
        
    steps = TransactionStep.query.filter_by(transaction_id= transaction.id).all()
    steps_list = [step.to_dict() for step in steps]    
    return jsonify({"steps": steps_list}), 200
    
  except SQLAlchemyError as e:
    return jsonify({'message': 'Database error occurred while fetching transaction steps', 'error': str(e)}), 500
    
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while fetching transaction steps', 'error': str(e)}), 500






