from flask import Blueprint, flash, redirect, render_template, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from app import admin, db
from app.forms import LoginForm, NewMajorForm, NewMajorSubjectForm, NewRoomForm, NewUserForm
from app.helper import delete_picture, upload_picture
from app.models import QA, ClassRequest, MajorSubject, Support, User, Announcement, Subject, Major, Room, College
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    current_user,
    logout_user,   
    )
from flask_admin.menu import MenuLink
from flask import get_flashed_messages
from flask_admin.form.upload import FileUploadField
from wtforms import PasswordField


admin_bp = Blueprint('admin_bp', __name__)


class MyModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin == True
 

class MyAdminIndexView(AdminIndexView):
   def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin == True
 
   
############################## User ################################

class UserAdmin(MyModelView):
  
  column_list = ['fullname','email','number','major.name', 'verified', 'is_admin','phone']
  column_searchable_list = ['fullname', 'email']
  form_excluded_columns = ('password','img_url')
  page_size = 20
  column_labels = {"major.name":"Major"}
  form_extra_fields = {
        'file_path': FileUploadField('Profile image',
                                      base_path='/path/to/upload',
                                      allowed_extensions=['jpg', 'png']),
        'password2': PasswordField('Password')
                      }

  def create_form(self, obj=None): 
    return NewUserForm()
  
  def on_model_change(self, form, model, is_created):
    try:

      if form.password2.data != '':
        model.password = generate_password_hash(form.password2.data)
      
      
      if form.email.data != model.email:  # Email changed
       if self.model_class.query.filter_by(email = form.email.data).first():
        flash("Email already exists!", "error")
        return False  # Prevent saving
       
      if not is_created and form.file_path.data:

        if model.img_url != 'default_image.jpg':
          delete_picture('app/static/images/user-images/', model.img_url) 
        filename = upload_picture(form.file_path.data, 'app/static/images/user-images/', (250,250))
        model.img_url = filename

      return super().on_model_change(form, model, is_created)
    
    except Exception as e:
      flash(f"An error occurred while saving the model: {str(e)}", "error")


  def delete_model(self, model):
    try:
      self.session.delete(model)
      self.session.commit()
      flash('Course was successfully deleted.', 'success')
      
    except Exception as ex:
      flash(f'Error deleting user: {str(ex)}', 'error')
      self.session.rollback()
      return False
    
    if model.img_url != 'default_image.jpg':
      delete_picture('app/static/images/user-images/', model.img_url) 
    
    return True
  
############################## Announcement ################################

class AnnouncementAdmin(MyModelView):
  column_list = ['title','content','date_posted']
  column_searchable_list = ['title']
  form_excluded_columns = ('date_posted','img_url')
  page_size = 10
  form_extra_fields = {
    'file_path': FileUploadField('Announcement image',
                                 base_path='/path/to/upload',
                                 allowed_extensions=['jpg', 'png']) 
                      }
  
  def on_model_change(self, form, model, is_created):
    try:  
      if form.file_path.data:
        if not is_created and model.img_url != 'default_image.jpg':
          delete_picture('app/static/images/announ-images/', model.img_url) 

        filename = upload_picture(form.file_path.data, 'app/static/images/announ-images/', (350,350))
        model.img_url = filename
        
      return super().on_model_change(form, model, is_created)
    
    except Exception as e:
      flash(f"An error occurred while saving the model: {str(e)}", "error")
  
  def delete_model(self, model):
    try:
      self.session.delete(model)
      self.session.commit()
      
    except Exception as ex:
      flash(f'Error deleting user: {str(ex)}', 'error')
      self.session.rollback()
      return False
    
    if model.img_url != 'default_image.jpg':
      delete_picture('app/static/images/announ-images/', model.img_url) 

    return True


############################## Subject ################################

class SubjectAdmin(MyModelView):
  column_searchable_list = ['name']
  page_size = 20

############################## Major ################################

class MajorAdmin(MyModelView):
  column_list = ['name','college.name']
  column_searchable_list = ['name']
  page_size = 20
  column_labels = {"college.name":"College"}

  def create_form(self, obj=None): 
    return NewMajorForm()
  

############################## Room ################################

class RoomAdmin(MyModelView):
  column_list = ['name', 'direction', 'college.name']
  column_searchable_list = ['name']
  page_size = 20
  column_labels = {"college.name":"College"}

  def create_form(self, obj=None): 
    return NewRoomForm() 


############################## Class Request ################################ 

class ClassRequestAdmin(MyModelView):
  column_list = ['user.fullname', 'user.number', 'subject.name']
  column_searchable_list = ['user.fullname', 'user.number', 'subject.name']
  column_labels = {
        'user.fullname': 'Student Name',
        'user.number': 'Student Number',
        'subject.name': 'Subject Name'
    }
  can_create = False  
  can_edit = False    

  page_size = 20


############################## MajorSubject ################################ 

class MajorSubjectAdmin(MyModelView):
  column_list = ['major.name', 'subject.name', 'num_of_hours', 'year', 'semester']
  column_searchable_list = ['major.name', 'subject.name']
  column_labels = {
        'major.name': 'Major Name',
        'subject.name': 'Subject Name'
    }    
  page_size = 20

  def create_form(self, obj=None): 
    return NewMajorSubjectForm() 
  
  def update_form(self, obj=None):
        
    form = super(MajorSubjectAdmin, self).update_form(obj)  
    form.major.name.render_kw = {'readonly': True}
    form.subject.name.render_kw = {'readonly': True}  
    return form

  def scaffold_form(self):
    form_class = super(MajorSubjectAdmin, self).scaffold_form()  
    del form_class.major
    del form_class.subject  
    return form_class
  
############################## Class Request ################################ 

class SupportAdmin(MyModelView):
  column_searchable_list = ['issue', 'title']
  can_create = False  
  can_edit = False    
  page_size = 20


admin.add_view(UserAdmin(User, db.session))
admin.add_view(AnnouncementAdmin(Announcement, db.session))
admin.add_view(SubjectAdmin(Subject, db.session))
admin.add_view(MajorAdmin(Major, db.session))
admin.add_view(RoomAdmin(Room, db.session))
admin.add_view(MyModelView(College, db.session))
admin.add_view(MyModelView(QA, db.session))
admin.add_view(ClassRequestAdmin(ClassRequest, db.session))
admin.add_view(MajorSubjectAdmin(MajorSubject, db.session))
admin.add_view(SupportAdmin(Support, db.session))

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

