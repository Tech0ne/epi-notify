from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from models import Hook
from db import session

def delete_expired_hooks():
    for hook in session.query(Hook).filter(Hook.expires_at <= datetime.now()).all():
        session.delete(hook)

    session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_hooks, 'interval', seconds=3600)