from flask_mail import Message
from app import mail

def send_email(subject, recipient, body):
    msg = Message(subject, sender='your_email@example.com', recipients=[recipient])
    msg.body = body
    mail.send(msg)