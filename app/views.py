from app import application, db, models, forms, user_datastore#, login_manager
from app.forms import LoginForm, RegistrationForm, CategorySubmissionForm, ChannelCreationForm, EventSubmissionForm
from app.models import *
from flask import render_template, request, jsonify, flash, redirect, url_for, Markup
from flask_security import current_user, login_user, login_required, logout_user
from flask_security.utils import hash_password, verify_and_update_password
from flask_security.decorators import roles_required, roles_accepted
from datetime import datetime
from sqlalchemy import desc
import json


@application.route('/')
def home_page():
	return render_template('index.html')

''' ************************************
	LOGIN / REGISTRATION
	************************************'''

# @application.login_manager.user_loader
# def load_user(id):
# 	return User.query.get(int(id))

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@application.route('/login', methods=['GET', 'POST'])
def login():
    # validate login
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if verify_and_update_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')	# checks for redirect
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_page')
        return redirect(next_page)

    return render_template('login.html', form=form)

@application.route('/register', methods=['GET', 'POST'])
@roles_accepted('admin', 'moderator')						# DELETE THIS!
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_datastore.create_user(username=form.username.data, email=form.email.data,
        			password=hash_password(form.password.data),
        			firstname=form.firstname.data, lastname=form.lastname.data,
        			created_at=datetime.utcnow(), login_count=0)

        db.session.commit()
        flash('You have successfully registered your account!')
        return redirect(url_for('home_page'))
    return render_template('register.html', title='Register', form=form)


''' ************************************
	PAGE CREATION
	************************************'''

# form to submit a new category
@application.route('/category_submission', methods=['GET', 'POST'])
@roles_accepted('admin', 'moderator')
def category_submission():
	if request.method == 'POST':
		form = CategorySubmissionForm()
		if form.validate_on_submit():
			#  add new category to db
			category = Category(title=form.category_title.data, category_type=form.category_type.data,
				created_at=datetime.utcnow())
			db.session.add(category)

			# iterate through each selected parent category and add a link to the db
			for cat in form.parent_category.data:
				categorylink = LinkToCategory(title_from=category.title, namespace_from="category",
					title_to=cat.title, created_at=datetime.utcnow())
				db.session.add(categorylink)
			db.session.commit()

			# redirect to newly created category
			flash('New category created!')
			return redirect(url_for('category_page', page_title=category.title))
	else:
		# adds params to form, if provided
		form = CategorySubmissionForm(request.args)
	return render_template('category_submission.html', title='Submit New Category', form=form)

# create channel from an existing category
@application.route('/create_channel', methods=['GET', 'POST'])
@roles_accepted('admin')
def create_channel():
	if request.method == 'POST':
		form = ChannelCreationForm()
		if form.validate_on_submit():
			channel = Channel(id_cat=form.category_for_channel.data.id, created_at=datetime.utcnow())
			db.session.add(channel)
			db.session.commit()

			title = form.category_for_channel.data.title

			# redirect to newly created channel
			flash('New channel created!')
			return redirect(url_for('channel_page', page_title=title))
	else:
		# adds params to form, if provided
		form = ChannelCreationForm(request.args)
	return render_template('create_channel.html', title='Create Channel', form=form)

# create event
@application.route('/event_submission', methods=['GET', 'POST'])
@roles_accepted('admin', 'moderator')
def event_submission():
	if request.method == 'POST':
		form = EventSubmissionForm()
		if form.validate_on_submit():
			event = Event(title=form.event_title.data, start_time=form.start_time.data,
				end_time=form.end_time.data, event_type=form.event_type.data, created_at=datetime.utcnow())
			db.session.add(event)
			
			# iterate through each selected parent category and add a link to the db
			for cat in form.parent_category.data:
				categorylink = LinkToCategory(title_from=event.title, namespace_from="event",
					title_to=cat.title, created_at=datetime.utcnow())
				db.session.add(categorylink)
			
			db.session.commit()

			# redirect to newly created category
			flash('New event created!')
			return redirect(url_for('event_page', page_title=event.title))
	else:
		# adds params to form, if provided
		form = EventSubmissionForm(request.args)
	return render_template('event_submission.html', title='Submit New Category', form=form)


''' ************************************
	PAGE VIEWS
	************************************'''

# view for category page
@application.route('/category/<page_title>/', methods=['GET'])
def category_page(page_title):
	# redirect if url has spaces (we convert them to underscores for friendlier urls)
	if ' ' in page_title:
		return redirect(url_for('category_page', page_title=page_title.replace(' ', '_')))

	page_exists = False 					# boolean used to track if the category page exsits
	is_channel = False
	parent_categories = []					# array used to track parent categories for the queried category
	subcategories = []
	events = []
	title = page_title.replace('_', ' ')	# replace underscores with spaces
	category_page = Category.query.filter_by(title=title).first()

	if category_page is not None:
		page_exists = True

		# query to see if the category has a channel page
		if Channel.query.filter_by(id_cat=category_page.id).first() is not None:
			is_channel = True
		
		title = category_page.title 	# fixes any capitalization errors

		# get parent categories
		parent_categories = [link.title_to for link in get_parent_cats_for_page(title)]

		# get subcategories
		subcategories = [link.title_from for link in get_subcats_for_page("category", title)]

		# get events
		events = [event.title for event in get_events_for_page("event", title)]

	return render_template('category_page.html', title=title, page_exists=page_exists,
		is_channel=is_channel, parent_categories=parent_categories, subcategories=subcategories,
		events=events)

# view for channel page
@application.route('/channel/<page_title>/', methods=['GET'])
@application.route('/<page_title>/', methods=['GET'])
def channel_page(page_title):
	# redirect if url has spaces (we convert them to underscores for friendlier urls)
	if ' ' in page_title:
		return redirect(url_for('channel_page', page_title=page_title.replace(' ', '_')))

	parent_categories = []					# array used to track parent categories for the queried category
	subcategories = []
	title = page_title.replace('_', ' ')	# replace underscores with spaces
	
	# look for the category page of the channel, which contains the metadata
	category_page = Category.query.filter_by(title=title).first()

	# if no channel page, redirect to category
	if category_page is None:
		return redirect(url_for('category_page', page_title=title))
	else:
		# checks to see if a channel has been made
		channel_page = Channel.query.get(category_page.id)
		
		if channel_page is None:
			return redirect(url_for('category_page', page_title=title))

		title = category_page.title 	# fixes any capitalization errors

		# get parent categories
		parent_categories = [link.title_to for link in get_parent_cats_for_page(title)]

		# get subcategories
		subcategories = [link.title_from for link in get_subcats_for_page("category", title)]

		# get events
		events = [event.title for event in get_events_for_page("event", title)]

		return render_template('channel_page.html', title=title, parent_categories=parent_categories,
			subcategories=subcategories, events=events)

# view for category page
@application.route('/event/<page_title>/', methods=['GET'])
def event_page(page_title):
	# redirect if url has spaces (we convert them to underscores for friendlier urls)
	if ' ' in page_title:
		return redirect(url_for('event_page', page_title=page_title.replace(' ', '_')))

	page_exists = False 					# boolean used to track if the category page exsits
	parent_categories = []					# array used to track parent categories for the queried category
	subcategories = []
	title = page_title.replace('_', ' ')	# replace underscores with spaces
	event_page = Event.query.filter_by(title=title).first()

	if event_page is not None:
		page_exists = True
		
		title = event_page.title 	# fixes any capitalization errors

		# get parent categories
		parent_categories = [link.title_to for link in get_parent_cats_for_page(title)]

		# get all videos
		videos = [v.url_test for v in get_videos_for_event(title)]

	return render_template('event_page.html', title=title, page_exists=page_exists,
		parent_categories=parent_categories, videos=videos)


def get_parent_cats_for_page(title):
	return LinkToCategory.query.filter_by(title_from=title).all()

def get_subcats_for_page(namespace_from, title):
	return LinkToCategory.query.filter_by(namespace_from=namespace_from, title_to=title).all()

def get_events_for_page(namespace_from, title):
	return Event.query.join(LinkToCategory, Event.title==LinkToCategory.title_from).filter_by(namespace_from=namespace_from,
		title_to=title).all()

def get_videos_for_event(title):
	return Video.query.\
		join(VideoLink, Video.id==VideoLink.video_from).\
		join(Event, VideoLink.event_to==Event.id).filter_by(title=title).all()
