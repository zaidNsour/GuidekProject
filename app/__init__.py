from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
admin = Admin( name='My Admin Panel', template_mode='bootstrap3')

login_manager = LoginManager()
login_manager.login_view = "admins.login"
login_manager.login_message_category = "info"

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')

 
  from app.rotues.admins import MyAdminIndexView

  db.init_app(app)
  migrate.init_app(app, db)
  jwt.init_app(app)
  mail.init_app(app)
  admin.init_app(app, index_view= MyAdminIndexView())
  login_manager.init_app(app)

  from app.rotues import auth,announcements, users, subjects, admins, majors, rooms
  from app.scheduler import start_scheduler
  from app.models import TokenBlocklist


  app.register_blueprint(auth.auth_bp)
  app.register_blueprint(announcements.announ_bp)
  app.register_blueprint(subjects.subject_bp)
  app.register_blueprint(users.user_bp)
  app.register_blueprint(admins.admin_bp)
  app.register_blueprint(majors.major_bp)
  app.register_blueprint(rooms.room_bp)

  with app.app_context():
  # Create the database if it doesn't exist
    db.create_all()
    

  # Callback function to check if a JWT exists in the database blocklist
  @jwt.token_in_blocklist_loader
  def check_if_token_revoked(jwt_header, jwt_data):
    jti = jwt_data["jti"]
    token = db.session.query(TokenBlocklist).filter_by(jti = jti).scalar()
    return token is not None 
  
  start_scheduler()

  return app


