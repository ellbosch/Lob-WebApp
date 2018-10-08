from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateTimeField
from app.models import *


# get all category choices
def get_all_categories():
	return Category.query.all()

# def get_categories_by_type(category_type):
# 	return Category.query.filter_by(category_type=category_type).all()

# def get_teams_for_league(league):
# 	rows = Category.query.filter_by(category_type="sports_team").join(LinkToCategory, LinkToCategory.title_from==Category.title).filter_by(title_to="%s Teams" % (league)).all()


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
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
	parent_category = QuerySelectMultipleField(label='Parent Category',
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

	event_type = SelectField('Event Type', choices=event_type_choices, coerce=str)
	event_title = StringField('New Event Title', validators=[DataRequired()])
	start_time = DateTimeField('Start Date', validators=[DataRequired()])
	end_time = DateTimeField('End Date (Optional)')
	parent_category = QuerySelectMultipleField(label='Parent Category',
		query_factory=get_all_categories, get_label='title', validators=[DataRequired()])
	submit = SubmitField('Submit')

	def check_datetime(self, start_time):
		print(start_time)
		print(type(start_time))
