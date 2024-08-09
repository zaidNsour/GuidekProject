from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_admin import Admin


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
admin = Admin( name='My Admin Panel', template_mode='bootstrap3')


def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')

  db.init_app(app)
  migrate.init_app(app, db)
  jwt.init_app(app)
  mail.init_app(app)
  #admin.init_app(app, index_view= MyAdminIndexView())

  from app.rotues import auth, profile, classes, admin, announcements, users, subjects
  from app.scheduler import start_scheduler
  from app.models import TokenBlocklist


  app.register_blueprint(auth.auth_bp)
  app.register_blueprint(announcements.announ_bp)
  app.register_blueprint(subjects.subject_bp)
  app.register_blueprint(users.user_bp)



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


