from app import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta
# from dateutil import tz
import enum


# helper functions
# def convert_to_utc(timestamp):
#     from_zone = tz.tzutc()
#     to_zone = tz.tzlocal()

#     utc = timestamp.replace(tzinfo=from_zone)
#     local = utc.astimezone(to_zone)
#     return local


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
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# channels have a 1-to-many mapping to categories--they are category pages converted into video consumption experiences
class Channel(db.Model):
    id_cat = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, nullable=False, unique=True)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime)
    event_type = db.Column(db.Enum(EventType), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # @hybrid_property
    # def start_time_local(self):
    #     return convert_utc_to_local(self.start_time)

    # @hybrid_property
    # def end_time_local(self):
    #     return convert_utc_to_local(self.end_time)


# links either category or event pages to other categories, creating the orgaized structure of the site
class LinkToCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_from = db.Column(db.String(255), index=True, nullable=False)
    namespace_from = db.Column(db.Enum(Namespace), nullable=False)
    title_to = db.Column(db.String(255), index=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


"""
VIDEO TABLES
"""

# class for video
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    latest_title_id = db.Column(db.Integer, db.ForeignKey('video_text_revision.text_id'),\
        nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False)

# links video to an event page
class VideoLinkToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_from = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    event_to = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

# keep separate table for all text so we can keep track of revisions
class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

# keeps track of revisions to video title/description
class VideoTextRevision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_id = db.Column(db.Integer, db.ForeignKey('text.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    rev_comment = db.Column(db.String(255))
    is_minor_edit = db.Column(db.Boolean)
    rev_parent_id = db.Column(db.Integer, db.ForeignKey('video_text_revision.id'))


# sssshhhhhhhhh
# class RedditVideoIgnore(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     videopost_id = db.Column(db.Integer, db.ForeignKey('videopost.id'))

class Videopost(db.Model):
    __bind_key__ = 'scraped_video'
    id = db.Column(db.String(80), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    source = db.Column(db.String(80), nullable=False)
    league = db.Column(db.String(80), nullable=False, index=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.String(80))
    reddit_score = db.Column(db.Integer)
    reddit_comments_url = db.Column(db.String(80))
    url = db.Column(db.String(200), nullable=False)
    mp4_url = db.Column(db.String(200), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    in_train_set = db.Column(db.Boolean, nullable=False)

    def __init__(self, id=None, title=None, source=None, league=None, date_posted=None, author=None,
                reddit_score=None, reddit_comments_url=None, url=None, in_train_set=0):
        self.id = id
        self.title = title
        self.source = source
        self.league = league
        self.date_posted = date_posted
        self.author = author
        self.reddit_score = reddit_score
        self.reddit_comments_url = reddit_comments_url
        self.url = url
        self.in_train_set = in_train_set

    def set_dimension(self, height=height, width=width):
        self.height = height
        self.width = width

    def set_mp4_url(self, mp4_url):
        self.mp4_url = mp4_url


    # @hybrid_property
    # def date_posted_utc(self):
    #     return self.date_posted + timedelta(hours=1)

    # serialize for json consumption
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'mp4_url': self.mp4_url,
            'league': self.league,
            'date_posted': self.date_posted,
            'author': self.author,
            'reddit_comments_url': self.reddit_comments_url,
            'reddit_score': self.reddit_score
        }












