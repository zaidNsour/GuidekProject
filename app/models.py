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
  major_id = db.Column(db.Integer, db.ForeignKey("major.id"), nullable=True) 

  fullname = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  verified = db.Column(db.Boolean, nullable=False, default=False)
  is_admin = db.Column(db.Boolean, nullable=False, default=True)

  #optional attributes
  verification_code = db.Column(db.Integer, nullable=True)
  date_of_birth = db.Column(db.DateTime, nullable=True)
  phone = db.Column(db.String(20), nullable=True)
  bio = db.Column(db.Text, nullable=True)
  img_url = db.Column(db.String(20), nullable=False, default="default_image.jpg")

  def __repr__(self):
     return f'User({self.fullname}, {self.email})'
  
  def to_dict(self):

    if self.major:
      return {
        "id": self.id,
        "major":self.major.name,
        "fullname": self.fullname,
        "email": self.email,
        "verified": self.verified,
        "date_of_birth": self.date_of_birth,
        "bio": self.bio,
        "phone": self.phone,
        "img_url": self.img_url,
  		  }
    else:
       return {
        "id": self.id,
        "major":None,
        "fullname": self.fullname,
        "email": self.email,
        "verified": self.verified,
        "date_of_birth": self.date_of_birth,
        "bio": self.bio,
        "phone": self.phone,
        "img_url": self.img_url,
       }
  
  def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({'user_id': self.id})

  @staticmethod
  def verify_reset_token(token, age=3600):
    s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
    try:
      user_id = s.loads(token, max_age=age)['user_id']
    except:
      return None
    return User.query.get(user_id)
  

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
  college_id = db.Column(db.Integer, db.ForeignKey("college.id"), nullable=False)

  name = db.Column(db.String(120), nullable=False)
  num_of_hours = db.Column(db.Integer)
  def to_dict(self):
    return {"name": self.name,"num_of_hours": self.num_of_hours}   
     
  def __repr__(self):
    return f' Subject({self.name})' 
  

class Major(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  college_id = db.Column(db.Integer, db.ForeignKey("college.id"), nullable=False) 


  name = db.Column(db.String(60), nullable=False)
  students = db.relationship('User', backref=db.backref('major', lazy=True))

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
   name = db.Column(db.String(30), nullable=False)
   college_id = db.Column(db.Integer, db.ForeignKey("college.id"), nullable=False) 
   direction = db.Column(db.String(120), nullable=False)
   

class College(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  location = db.Column(db.String(120), nullable=False)

  majors = db.relationship('Major', backref=db.backref('college', lazy=True))
  subjects = db.relationship('Subject', backref=db.backref('college', lazy=True))
  rooms = db.relationship('Room', backref=db.backref('college', lazy=True))


class QA(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   question = db.Column(db.String(120), nullable=False)
   answer = db.Column(db.String(120), nullable=False)





   
    
        
  









