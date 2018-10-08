from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
import os

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Cupcake2777@lobdb.czfflgcbpl6i.us-west-2.rds.amazonaws.com:3306/lobdb?charset=utf8mb4?collate=utf8mb4_unicode_ci'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'lob-sicrit-key'
# application.config['SECURITY_CONFIRMABLE'] = True # UNCOMMENT THIS WHEN EMAIL CONFIRMATION IS ADDED
application.config['SECURITY_TRACKABLE'] = True
application.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
application.config['SECURITY_PASSWORD_SALT'] = 'super-sicrit-salt'


db = SQLAlchemy(application)

from app import models			# import model BEFORE creating tables and after db, otherwise it breaks




# DELETE THIS: drop tables
# from app.models import * 
# LinkToCategory.__table__.drop(db.engine)
# Channel.__table__.drop(db.engine)
# Event.__table__.drop(db.engine)
# Category.__table__.drop(db.engine)





db.create_all() 				# In case user table doesn't exists already. Else remove it.    
db.session.commit() 			# This is needed to write the changes to database

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(application, user_datastore)



# DELETE DIS
# create moderator and admin roles
# user_datastore.create_role(name='admin')
# user_datastore.create_role(name='moderator')

# from flask_security.utils import hash_password
# from datetime import datetime
# with application.app_context():
# 	user_datastore.create_user(username='admin', email='admin@lob.tv',
# 					password=hash_password('Cupcake2777'), roles=['admin'],
# 					firstname="lebron", lastname="james", 
# 					created_at=datetime.utcnow(), login_count=0)
# 	db.session.commit()



# from datetime import datetime
# sports_cat = Category(title="Sports", category_type="default", created_at=datetime.utcnow())
# baseball_cat = Category(title="Baseball", category_type="default", created_at=datetime.utcnow())
# mlb_cat = Category(title="MLB", category_type="sports_league", created_at=datetime.utcnow())
# season_cat = Category(title="MLB Teams", category_type="default", created_at=datetime.utcnow())
# braves = Category(title="Atlanta Braves", category_type="sports_team", created_at=datetime.utcnow())
# dodgers = Category(title="Los Angeles Dodgers", category_type="sports_team", created_at=datetime.utcnow())
# event = Event(title="Event Test", start_time="2018-04-13 10:03:08", event_type="sports_game", created_at=datetime.utcnow())

# link1 = LinkToCategory(title_from="Baseball", namespace_from="category", title_to="Sports", created_at=datetime.utcnow())
# link2 = LinkToCategory(title_from="MLB", namespace_from="category", title_to="Baseball", created_at=datetime.utcnow())
# link3 = LinkToCategory(title_from="MLB Teams", namespace_from="category", title_to="MLB", created_at=datetime.utcnow())
# link4 = LinkToCategory(title_from="Atlanta Braves", namespace_from="category", title_to="MLB Teams", created_at=datetime.utcnow())
# link5 = LinkToCategory(title_from="Los Angeles Dodgers", namespace_from="category", title_to="MLB Teams", created_at=datetime.utcnow())
# link6 = LinkToCategory(title_from="Event Test", namespace_from="event", title_to="Los Angeles Dodgers", created_at=datetime.utcnow())
# link7 = LinkToCategory(title_from="Event Test", namespace_from="event", title_to="Atlanta Braves", created_at=datetime.utcnow())

# db.session.add(sports_cat)
# db.session.add(baseball_cat)
# db.session.add(mlb_cat)
# db.session.add(season_cat)
# db.session.add(braves)
# db.session.add(dodgers)
# db.session.add(event)
# db.session.add(link1)
# db.session.add(link2)
# db.session.add(link3)
# db.session.add(link4)
# db.session.add(link5)
# db.session.add(link6)
# db.session.add(link7)
# db.session.commit()

from app import views