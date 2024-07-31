from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()


def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')

  db.init_app(app)
  migrate.init_app(app, db)
  jwt.init_app(app)
  mail.init_app(app)

  from app.rotues import auth, profile, classes, admin, announcements, users, subjects
  app.register_blueprint(auth.auth_bp)
  app.register_blueprint(announcements.announ_bp)
  app.register_blueprint(subjects.subject_bp)
  app.register_blueprint(users.user_bp)


  with app.app_context():
  # Create the database if it doesn't exist
    db.create_all()

  return app


