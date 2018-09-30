from app import db
from models import User, Admin

def add(username):
	user = User.query.filter_by(username=username).first()
	admin = Admin(user_id=user.id)
	db.session.add(admin)
	db.session.commit()
