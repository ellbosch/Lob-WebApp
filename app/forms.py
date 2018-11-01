from app.models import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField, RadioField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateTimeField
from flask_security.forms import LoginForm


"""
QUERIES FOR QUERY SELECTORS
"""
def get_all_categories():
	return Category.query.order_by(Category.title).all()

def get_all_events():
	return Event.query.order_by(db.desc(Event.start_time)).all()

def get_all_leagues():
	return Category.query.filter_by(category_type="sports_league").\
		order_by(Category.title).all()

def get_all_teams():
	return Category.query.filter_by(category_type="sports_team").\
		order_by(Category.title).all()

# def get_roles():
# 	return Role.query.all()

"""
HELPER FUNCTIONS
"""

# ensure video is .mp4
def validate_video_url(form, video_url):
	# check if format is correct
	if not video_url.data.endswith('.mp4'):
		raise ValidationError('Video must be in .mp4 format.')

	# check if same video has already been uploaded
	v = Video.query.filter_by(url=video_url.data).first()
	if v != None:
		print("just making sure")
		raise ValidationError("This video has already been uploaded.")


"""
FORM CLASSES
"""

class ExtendedLoginForm(LoginForm):
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		print(user)
		if user == None:
			raise ValidationError('Invalid password.')

	# username = StringField('Username', validators=[DataRequired()])
	# password = PasswordField('Password', validators=[DataRequired()])
	# remember_me = BooleanField('Remember Me')
	# submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(),
		EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already taken! Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email address already taken! Please use a different email.')

class CategorySubmissionForm(FlaskForm):
	# choices for category type
	category_type_choices = [
		("default", 'Default'),
		("sports_league", "Sports - League"),
		("sports_team", 'Sports - Team'),
		("sports_player", 'Sports - Player')
	]

	category_title = StringField('New Category Title', validators=[DataRequired()])
	category_type = SelectField('Category Type', choices=category_type_choices, coerce=str)
	parent_category = QuerySelectMultipleField(label='Parent Categories',
		query_factory=get_all_categories, get_label='title', validators=[DataRequired()])
	submit = SubmitField('Submit')

	def validate_category_title(self, category_title):
		# check if page contains invalid characters (like underscores)
		if '_' in category_title.data:
			raise ValidationError('Category title cannot contain underscores! Please replace underscores with spaces.')

		# check if category is already made
		page = Category.query.filter_by(title=category_title.data).first()
		if page is not None:
			raise ValidationError('Category title already taken! Please use a different name.')

	def check_for_duplicates(self, category_title, parent_category):
		for cat in parent_category:
			results = LinkToCategory.query.filter_by(title_from=category_title, namespace_from="category",
				title_to=cat.title).all()
			if len(results) > 0:
				titles = [cat.title for cat in results]
				raise ValidationError('This category has already been linked to: %s' % titles)

class ChannelCreationForm(FlaskForm):
	category_for_channel = QuerySelectField(label='Make Channel for Category',
		query_factory=get_all_categories, get_label='title',
		validators=[DataRequired()])
	submit = SubmitField('Submit')

class EventSubmissionForm(FlaskForm):
	# choices for event type
	event_type_choices = [
		("default", 'Default'),
		("sports_game", 'Sports - Game')
	]

	event_type = RadioField('Event Type', choices=event_type_choices, coerce=str, default="sports_game")

	# for default event
	event_title = StringField('New Event Title')

	# for sports game matchup: automatically generate title name
	# league = SelectField('Select League', choices=[("","-- Select League --")], coerce=str)
	league = QuerySelectField('Select League', query_factory=get_all_leagues,
		get_label='title')

	# away_team = SelectField('Select Away Team',
	# 	coerce=str)
	# home_team = SelectField('Select Home Team',
	# 	coerce=str)
	away_team = QuerySelectField('Select Away Team', query_factory=get_all_teams,
		get_label='title')
	home_team = QuerySelectField('Select Home Team', query_factory=get_all_teams,
		get_label='title')

	start_time = StringField('Start Date', validators=[DataRequired()])
	end_time = StringField('End Date (Optional)')
	parent_category = QuerySelectMultipleField(label='Parent Categories',
		query_factory=get_all_categories, get_label='title')
	tz = StringField('Time Zone')		# hidden input that stores time zone

	submit = SubmitField('Submit')


class VideoSubmissionForm(FlaskForm):
	video_url = StringField('Video Link (must be .mp4)', validators=[DataRequired(), validate_video_url])
	video_title = StringField('Video Title', validators=[DataRequired()])
	parent_events = QuerySelectMultipleField(label='Upload to Event Pages',
		query_factory=get_all_events, get_label='title', validators=[DataRequired()])

	submit = SubmitField('Submit')

class UserRoleForm(FlaskForm):
	# roles = QuerySelectMultipleField(label='Select Roles', query_factory=get_roles,
		# get_label='name', default=["3"])
	is_beta_user = BooleanField('Beta User')
	is_scraper = BooleanField('Scraper')
	is_moderator = BooleanField('Moderator')
	is_admin = BooleanField('Admin')

