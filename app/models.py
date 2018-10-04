from app import db
from flask_security import UserMixin, RoleMixin
import enum

"""
USER TABLES
"""

# define model for users (comes from flask-security)
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

# basic user, moderator, admin, etc.
class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

# user account class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


    def __repr__(self):
        return '<User {}>'.format(self.username)    


"""
PAGE TABLES
"""
class Namespace(enum.Enum):
    category = 1
    channel = 2
    event = 3

# pages can be anything from categories, channels, and events
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namespace = db.Column(db.Enum(Namespace), nullable=False, index=True)
    title = db.Column(db.String(255), unique=True, index=True, nullable=False)
    redirect = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, nullable=False)

# category links are links FROM pages TO category pages (i.e. FROM Baseball TO Sports)
class CategoryLink(db.Model):
    # DOUBLE CHECK MEDIAWIKI FOR BACKREFS
    id = db.Column(db.Integer, primary_key=True)
    id_from = db.Column(db.Integer, db.ForeignKey('page.id'), index=True, nullable=False)   # page where link is located
    id_to = db.Column(db.Integer, db.ForeignKey('page.id'), index=True, nullable=False)     # page where link sends to
    created_at = db.Column(db.DateTime, nullable=False)