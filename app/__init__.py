from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Cupcake2777@lobdb.czfflgcbpl6i.us-west-2.rds.amazonaws.com:3306/lobdb?charset=utf8mb4?collate=utf8mb4_unicode_ci'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'lob-sicrit-key'


db = SQLAlchemy(application)

from app import models				# import model BEFORE creating tables and after db, otherwise it breaks
db.create_all() 			# In case user table doesn't exists already. Else remove it.    
db.session.commit() 		# This is needed to write the changes to database

# setup login manager
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

from app import views

from app import admin
admin.add('ellbosch')