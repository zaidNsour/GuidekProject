from flask import current_app
from itsdangerous import Serializer
from . import db, login_manager
from datetime import datetime
from datetime import timedelta
from sqlalchemy.sql import func
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
  return User.query.get( int(user_id) )


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    # this need modify
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    expires_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Token<{self.jti}>'
    
    def __init__(self, jti, expires_in):
        self.jti = jti
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(seconds=expires_in)



class User(db.Model,UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  major_id = db.Column(db.Integer, db.ForeignKey("major.id"), nullable = False)
  email = db.Column(db.String(120), unique=True, nullable=False) 
  number = db.Column(db.String(20), unique=True, nullable=False)
  fullname = db.Column(db.String(80), nullable=False)
  password = db.Column(db.String(60), nullable=False)
  verified = db.Column(db.Boolean, nullable=False, default=False)
  is_admin = db.Column(db.Boolean, nullable=False, default=False)

  #optional attributes
  phone = db.Column(db.String(20), nullable=True)
  img_url = db.Column(db.String(20), nullable=False, default="default_image.jpg")

  requested_classes = db.relationship('Subject', secondary = 'class_request', backref = 'students_request')

  def __repr__(self):
     return f'User({self.fullname}, {self.number})'
  
  def to_dict(self):
    return {
      "id": self.id,
      "number":self.number,
      "major_name":self.major.name,
      "fullname": self.fullname,
      "email": self.email,
      "verified": self.verified,
      "phone": self.phone,
      "img_url": self.img_url,
       }
  
  def get_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({'user_id': self.id})

  @staticmethod
  def verify_token(token, age=3600):
    s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
    try:
      user_id = s.loads(token, max_age=age)['user_id']
    except:
      return None
    return User.query.get(user_id)
  

class ClassRequest(db.Model):
  __tablename__ = 'class_request'
  student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), primary_key=True)
  date_of_request = db.Column(db.DateTime, nullable=False, default= datetime.now)

'''
class ClassEnroll(db.Model):
  __tablename__ = 'class_enroll'
  student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  class_id = db.Column(db.Integer, db.ForeignKey('subject.id'), primary_key=True)
  date_of_enrolled = db.Column(db.DateTime, nullable=False, default= datetime.now)


class Class(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable = False)
  instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
  room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable = True)
  books = db.Column(db.Text, nullable = True)
  slides = db.Column(db.Text, nullable = True)
  course_plan = db.Column(db.Text, nullable = True)

'''

class Announcement(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  title = db.Column(db.String(120), nullable=False)
  content = db.Column(db.Text, nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
  img_url = db.Column(db.String(20), nullable=False, default="default_image.jpg")

  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "content": self.content,
      "date_posted": self.date_posted.isoformat(),
      "img_url": self.img_url
  		}
  

class Subject(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120),unique=True,nullable=False)
  book = db.Column(db.Text, nullable = True)
  slides = db.Column(db.Text, nullable = True)
  course_plan = db.Column(db.Text, nullable = True)
  
  def to_dict(self):
    return {"name": self.name}   
     
  def __repr__(self):
    return f' Subject({self.name})' 
    

class Major(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  college_id = db.Column(db.Integer, db.ForeignKey("college.id"), nullable=False) 

  name = db.Column(db.String(60), unique=True, nullable=False)
  students = db.relationship('User', backref=db.backref('major', lazy=True))
  subjects = db.relationship('Subject', secondary = 'major_subject', backref = 'majors')
  def to_dict(self):
    return {"name": self.name, "college_name":self.college.name} 
  

# add num_of_hours
class MajorSubject(db.Model):
    __tablename__ = 'major_subject'
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), primary_key=True)

    num_of_hours = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<MajorSubject {self.major_id}, {self.subject_id}, type = {self.type}>'
    
    def to_dict(self):
      return {"subject name": Subject.query.filter_by(id = self.subject_id).first().name,
            "num_of_hours": self.num_of_hours, 
            "year": self.year,
            "semester":self.semester
            }
    

class Room(db.Model):
   id = db.Column(db.Integer, primary_key=True)

   name = db.Column(db.String(30), unique=True, nullable=False)
   college_id = db.Column(db.Integer, db.ForeignKey("college.id"), nullable=False) 
   direction = db.Column(db.String(120), nullable=False)

   def to_dict(self):
    return {"name": self.name,"college_name": self.college.name, "direction": self.direction}


class College(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable = False)
  location = db.Column(db.String(120), nullable = False)

  majors = db.relationship('Major', backref=db.backref('college', lazy=True))
  rooms = db.relationship('Room', backref=db.backref('college', lazy=True))


class QA(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   question = db.Column(db.String(120), nullable=False)
   answer = db.Column(db.String(120), nullable=False)

   def to_dict(self):
    return {"question": self.question,"answer": self.answer}


class Transaction(db.Model):
   id = db.Column(db.Integer, primary_key=True)

   name = db.Column(db.String(80), unique=True, nullable = False)
   fee = db.Column(db.Float, nullable=False)
   expected_time = db.Column(db.Integer, nullable=False)

   steps = db.relationship('TransactionStep', backref=db.backref('transaction', lazy=True))
   def to_dict(self):
    return {"name": self.name,"fee": self.fee, "expected_time":self.expected_time}


class TransactionStep(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)

   number = db.Column(db.Integer, nullable=False)
   description = db.Column(db.String(120), nullable=False)

   def to_dict(self):
    return {"number": self.number,"description": self.description}

   '''
   @staticmethod
   def add_step(transaction_id, description):    
     last_step = TransactionStep.query.filter_by(transaction_id=transaction_id).order_by(TransactionStep.number.desc()).first()
     next_number = 1 if last_step is None else last_step.number + 1   
     new_step = TransactionStep(transaction_id=transaction_id, number=next_number, description=description)
     db.session.add(new_step)
     db.session.commit()
     return new_step
   '''

class Support(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_email = db.Column(db.String(80), nullable = False )
  issue = db.Column(db.String(80), nullable = False )
  title = db.Column( db.String(80), nullable = False )
  description = db.Column(db.Text, nullable = True)








   
   




   
    
        
  









