# script to manually add admins (call function from __init__.py)

from app import db, models
from app.models import User, Admin
from datetime import datetime

def add(username):
	user = User.query.filter_by(username=username).first()
	admin = Admin(user_id=user.id, timestamp_added=datetime.utcnow())
	db.session.add(admin)
	db.session.commit()
