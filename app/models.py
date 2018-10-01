from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# user account class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email_authenticated = db.Column(db.Boolean, nullable=False)
    timestamp_created = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# moderators can edit and delete content
class Moderator(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    timestamp_added = db.Column(db.DateTime, nullable=False)

# admins run the world
class Admin(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    timestamp_added = db.Column(db.DateTime, nullable=False)