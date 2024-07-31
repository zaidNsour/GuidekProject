from . import db
from datetime import datetime


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  fullname = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  verified = db.Column(db.Boolean, nullable=False, default=False)
  is_admin = db.Column(db.Boolean, nullable=False, default=False)

  #optional attributes
  verification_code = db.Column(db.Integer, nullable=True)
  date_of_birth = db.Column(db.DateTime, nullable=True)
  phone = db.Column(db.String(20), nullable=True)
  bio = db.Column(db.Text, nullable=True)
  img_url = db.Column(db.String(20), nullable=False, default="default_image.jpg")

  def __repr__(self):
     return f'User({self.fullname}, {self.email})'
  
  def to_dict(self):
    return {
      "id": self.id,
      "fullname": self.fullname,
      "email": self.email,
      "verified": self.verified,
      "date_of_birth": self.date_of_birth,
      "bio": self.bio,
      "phone": self.phone,
      "img_url": self.img_url,
  		}
  

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
  name = db.Column(db.String(120), nullable=False)
  num_of_hours = db.Column(db.Integer, primary_key=False)
  def to_dict(self):
    return {"name": self.name,"num_of_hours": self.num_of_hours}   
     
  def __repr__(self):
    return f' User({self.name})' 
      
	
class Collage(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
    
        
  









