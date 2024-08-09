import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY')
    # dont forget to modify that for security concern
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours = 6)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours = 12)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME= os.environ.get('EMAIL_USER')
    MAIL_PASSWORD= os.environ.get('EMAIL_PASS')