from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email
from wtforms.validators import Regexp, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from wtforms.validators import Regexp, ValidationError, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import College, Major, Subject, Transaction, TransactionStep, User

def choice_query_major():
  return Major.query 

def choice_query_college():
  return College.query
 
def choice_query_subject():
  return Subject.query

def choice_query_transaction():
  return Transaction.query


class ResetPasswordForm(FlaskForm):
  password=PasswordField(
      "password",
      validators=[ DataRequired(),Regexp("^(?=.*[A-Z])(?=.*[!@#$%^&*_\-()]).{8,30}$")]
    )
  confirm_password=PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")] )
  submit=SubmitField("Reset password")


class LoginForm(FlaskForm):
  email=StringField("Email", validators=[DataRequired(), Email()]  )
  password=PasswordField("Password", validators=[DataRequired()])
  submit=SubmitField("Login")

############################## Admin Forms ################################

class NewUserForm(FlaskForm):
  fullname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=25)])
  email = StringField("Email", validators=[DataRequired(), Email()] )
  number = StringField("Number", validators=[DataRequired(), Length(min=2, max=25)])
  major = QuerySelectField("Major", query_factory=choice_query_major, get_label="name")
  password2 = PasswordField(
      "password",
      validators=[ 
        DataRequired(),
        Regexp(
          "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{8,32}$"
          )
       ]
    )
  verified = BooleanField("Verified")
  is_admin = BooleanField("Is Admin")

  def validate_email(self, email):
    user=User.query.filter_by(email= email.data).first()
    if user:
      raise ValidationError("Email is already exist")


class NewMajorForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Length(min=2, max=25)])
  college = QuerySelectField("College", query_factory=choice_query_college, get_label="name")
 
  def validate_name(self, name):
    major = Major.query.filter_by(name= name.data).first()
    if major:
      raise ValidationError("Major is already exist")
    
    
class NewRoomForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Length(min=2, max=25)])
  direction = StringField("Direction", validators=[DataRequired(), Length(min=5, max=150)])
  college = QuerySelectField("College", query_factory=choice_query_college, get_label="name")
 
  def validate_name(self, name):
    major = Major.query.filter_by(name= name.data).first()
    if major:
      raise ValidationError("Major is already exist")
    

class NewMajorSubjectForm(FlaskForm):
  major = QuerySelectField("Major", query_factory=choice_query_major, get_label="name")
  subject = QuerySelectField("Subject", query_factory=choice_query_subject, get_label="name")
  num_of_hours = StringField("Num Of Hours", validators=[DataRequired(), Length(max= 1)])
  year = StringField("Year", validators=[DataRequired(), Length(max= 1)])
  semester = StringField("Semester", validators=[DataRequired(), Length(max= 1)])

  def validate_name(self, name):
    major = Major.query.filter_by(name= name.data).first()
    if major:
      raise ValidationError("Major is already exist")
    
    
class NewTransactionStepForm(FlaskForm):
  transaction = QuerySelectField("Transaction", query_factory=choice_query_transaction, get_label="name")
  number = StringField("Number", validators=[DataRequired(), Length(max= 1)])
  description = StringField("Description", validators=[DataRequired(), Length(max= 120)])

  def validate_number(self, number):
    t = Transaction.query.filter_by(name = self.transaction.data.name).first()
    transaction_step = TransactionStep.query.filter_by(transaction = t,number= number.data).first()
    if transaction_step:
      raise ValidationError("Number of this step in the transaction already exist.")
    
    

    

    
    