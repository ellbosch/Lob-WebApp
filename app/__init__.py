from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
import os

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Cupcake2777@lobdb.czfflgcbpl6i.us-west-2.rds.amazonaws.com:3306/lobdb?charset=utf8mb4?collate=utf8mb4_unicode_ci'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_BINDS'] = { 'scraped_video' : 'mysql://lebron_james:cupcake2777@thelobdb.czfflgcbpl6i.us-west-2.rds.amazonaws.com:3306/thelobdb?charset=utf8mb4?collate=utf8mb4_unicode_ci' }
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
from app.forms import ExtendedLoginForm
security = Security(application, user_datastore, login_form=ExtendedLoginForm)


from app.api.v0.routes import api_v0
from app.api.v1.routes import api_v1
application.register_blueprint(api_v0)
application.register_blueprint(api_v1, url_prefix='/api/v1')
