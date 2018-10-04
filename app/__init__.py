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
db.create_all() 				# In case user table doesn't exists already. Else remove it.    
db.session.commit() 			# This is needed to write the changes to database

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(application, user_datastore)

# DELETE DIS
# create moderator and admin roles
# user_datastore.create_role(name='admin')
# user_datastore.create_role(name='moderator')

# DELETE DIS
# add temp admin
# from flask_security.utils import hash_password
# from datetime import datetime
# with application.app_context():
# 	user_datastore.create_user(username='admin', email='admin@lob.tv',
# 					password=hash_password('Cupcake2777'), roles=['admin'],
# 					firstname="lebron", lastname="james", 
# 					created_at=datetime.utcnow(), login_count=0)
# 	db.session.commit()

# DELETE DIS
# sports category init
# from datetime import datetime
# sports_cat = models.Page(namespace="category", title="Sports", created_at=datetime.utcnow())
# db.session.add(sports_cat)
# db.session.commit()

from app import views