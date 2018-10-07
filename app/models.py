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
SPORTS DATA
"""
# class SportsTeamGame(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
#     away_team_cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
#     home_team_cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)


"""
PAGE TABLES
"""
class Namespace(enum.Enum):
    category = 1
    channel = 2
    event = 3

class EventType(enum.Enum):
    default = 1
    sports_game = 2

class CategoryType(enum.Enum):
    default = 1
    sports_league = 2
    sports_team = 3
    sports_player = 4

# category pages create the wiki-like hierarchy thoughout the site
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, index=True, nullable=False)
    category_type = db.Column(db.Enum(CategoryType), nullable=False)
    redirect = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, nullable=False)

# channels have a 1-to-many mapping to categories--they are category pages converted into video consumption experiences
class Channel(db.Model):
    id_cat = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime)
    event_type = db.Column(db.Enum(EventType), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

# links either category or event pages to other categories, creating the orgaized structure of the site
class LinkToCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_from = db.Column(db.String(255), index=True, nullable=False)
    namespace_from = db.Column(db.Enum(Namespace), nullable=False)
    title_to = db.Column(db.String(255), index=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
