from flask import Blueprint, flash, redirect, render_template, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from app import admin, db
from app.forms import LoginForm
from app.models import QA, ClassRequest, MajorSubject, User, Announcement, Subject, Major, Room, College
from werkzeug.security import  check_password_hash
from flask_login import (
    login_user,
    current_user,
    logout_user,   
    )
from flask_admin.menu import MenuLink
from flask import get_flashed_messages

admin_bp = Blueprint('admin_bp', __name__)



class MyModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin == True
 

class MyAdminIndexView(AdminIndexView):
   def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin == True
 
   

   
############################## User ################################
   
class UserAdmin(MyModelView):
  
  column_list = ['fullname','email', 'verified', 'is_admin','phone','img_url']
  column_searchable_list = ['fullname', 'email']
  form_excluded_columns = ('password')
  page_size = 20
  
############################## User ################################



admin.add_view(UserAdmin(User, db.session))
admin.add_view(MyModelView(Announcement, db.session))
admin.add_view(MyModelView(Subject, db.session))
admin.add_view(MyModelView(Major, db.session))
admin.add_view(MyModelView(Room, db.session))
admin.add_view(MyModelView(College, db.session))
admin.add_view(MyModelView(QA, db.session))
admin.add_view(MyModelView(ClassRequest, db.session))
admin.add_view(MyModelView(MajorSubject, db.session))

admin.add_link(MenuLink(name='Logout', category='', url="/logout"))




################################################ routes ######################################


@admin_bp.route("/login", methods=['GET', 'POST'])
def login():
    
    #if current_user.is_authenticated:
        #return redirect(url_for('admin.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data ).first()
       
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash("Invalid email or password", "error")
            # Pass the form back to the template with errors
            flash_messages = get_flashed_messages() 
            return render_template("login.html", title="Login", form = form,flash_messages= flash_messages)
             
    flash_messages = get_flashed_messages() 
    return render_template("login.html", title="Login",
                           form = form, flash_messages = flash_messages)


@admin_bp.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("admin_bp.login"))

################################################ routes ######################################