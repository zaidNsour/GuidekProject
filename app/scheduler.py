from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit
from app.models import  TokenBlocklist
from app import db

def delete_expired_tokens():
    now = datetime.now()
    expired_tokens = TokenBlocklist.query.filter(TokenBlocklist.expires_at < now).all()
    for token in expired_tokens:
        db.session.delete(token)
    db.session.commit()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_expired_tokens, trigger="interval", hours=1)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())