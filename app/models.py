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
  number = db.Column(db.Integer, unique=True, nullable=False)
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
  

class Subject(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  college_id = db.Column(db.Integer, db.ForeignKey("college.id"), nullable=False)

  name = db.Column(db.String(120),unique=True,nullable=False)
  num_of_hours = db.Column(db.Integer)
  def to_dict(self):
    return {"name": self.name,"num_of_hours": self.num_of_hours, "college_name":self.college.name}   
     
  def __repr__(self):
    return f' Subject({self.name})' 
  

class ClassRequest(db.Model):
  __tablename__ = 'class_request'
  student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), primary_key=True)
  date_of_request = db.Column(db.DateTime, nullable=False, default=datetime.now)
  
  
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
    


class Major(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  college_id = db.Column(db.Integer, db.ForeignKey("college.id"), nullable=False) 


  name = db.Column(db.String(60), unique=True, nullable=False)
  students = db.relationship('User', backref=db.backref('major', lazy=True))
  def to_dict(self):
    return {"name": self.name, "college_name":self.college.name} 
  

class MajorSubject(db.Model):
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), primary_key=True)

    type = db.Column(db.String(50), nullable=False)

    major = db.relationship('Major', backref=db.backref('major_subjects', cascade="all, delete-orphan"))
    subject = db.relationship('Subject', backref=db.backref('major_subjects', cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<MajorSubject {self.major_id}, {self.subject_id}, type = {self.type}>'
    

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
  subjects = db.relationship('Subject', backref=db.backref('college', lazy=True))
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


class TransactionStep(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)

   number = db.Column(db.Integer, nullable=False)
   description = db.Column(db.String(120), nullable=False)



   
    
        
  









