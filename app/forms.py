from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import *


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
	# get all category options
	entities = []
	for entity in Page.query.filter_by(namespace='category').all():
		entities.append((entity.id, entity.title))

	category_title = StringField('New Category Title', validators=[DataRequired()])
	parent_category = SelectField(label='Parent Category', choices=entities, coerce=int, validators=[DataRequired()])
	submit = SubmitField('Submit')

	def validate_category_title(self, category_title):
		# check if page contains invalid characters (like underscores)
		if '_' in category_title.data:
			raise ValidationError('Category title cannot contain underscores! Please replace underscores with spaces.')

		# check if page is already made
		page = Page.query.filter_by(namespace='category', title=category_title.data).first()
		if page is not None:
			raise ValidationError('Category title already taken! Please use a different name.')