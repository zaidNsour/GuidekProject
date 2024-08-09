from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Email
from wtforms.validators import Regexp, EqualTo


class ResetPasswordForm(FlaskForm):
  password=PasswordField(
      "password",
      validators=[ 
        DataRequired(),

        
          Regexp("^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,30}$")
       
        
       ]
    )
  confirm_password=PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")] )
  submit=SubmitField("Reset password")