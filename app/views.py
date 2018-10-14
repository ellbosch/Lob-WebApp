from app import application, db, models, forms, user_datastore, sample_data
from app.forms import LoginForm, RegistrationForm, CategorySubmissionForm, ChannelCreationForm, EventSubmissionForm, VideoSubmissionForm
from app.models import *
from flask import render_template, request, jsonify, flash, redirect, url_for, Markup
from flask_security import current_user, login_user, login_required, logout_user
from flask_security.utils import hash_password, verify_and_update_password
from flask_security.decorators import roles_required, roles_accepted
from datetime import datetime, timedelta
from sqlalchemy import desc
from collections import defaultdict
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

@application.route('/load_sample_data', methods=['GET', 'POST'])
def load_sample_data():
	if current_user.id != None:
		sample_data.load(current_user.id)

	return render_template('index.html')

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

# submit video
@application.route('/video_submission', methods=['GET', 'POST'])
@roles_accepted('admin', 'moderator')
def video_submission():
	if request.method == 'POST':
		form = VideoSubmissionForm()
		if form.validate_on_submit():
			text = Text(text=form.video_title.data)
			db.session.add(text)
			db.session.flush()		# updates db so we can get text.id

			# create text revision and event link after above is made
			text_rev = VideoTextRevision(text_id=text.id, timestamp=datetime.utcnow(),\
				created_by=current_user.id)
			db.session.add(text_rev)
			db.session.flush()		# updates db so we can get text_rev.id

			# create video and text rows
			video = Video(posted_by=current_user.id, url=form.video_url.data, height=-1,\
				width=-1, duration=-1, latest_title_id=text_rev.id)
			db.session.add(video)
			db.session.flush()

			# get all linked events from form
			for event in form.parent_events.data:
				e = Event.query
				video_link_to_event = VideoLinkToEvent(video_from=video.id, event_to=event.id,\
					score=0, created_by=current_user.id, created_at=datetime.utcnow())
				db.session.add(video_link_to_event)
			
			db.session.commit()

			flash('New video posted!')
			render_template('video_submission.html', title='Submit New Video', form=form)
			# return redirect(url_for('video_page', video_id=video.id))
	else:
		# adds params to form, if provided
		form = VideoSubmissionForm(request.args)
	return render_template('video_submission.html', title='Submit New Video', form=form)


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
		subcategories = [cat.title for cat in get_subcats_for_cat(title)]

		# get events
		events = [event.title for event in get_events_for_cat(title)]

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
		subcategories = [cat.title for cat in get_subcats_for_cat(title)]

		# get all nested events
		events = [event.title for event in get_nested_events_for_cat(category_page)]

		# get all videos for each event
		videos_per_event = {}
		for event in events:
			videos_per_event[event] = get_videos_for_event(event)

		return render_template('channel_page.html', title=title, parent_categories=parent_categories,
			subcategories=subcategories, events=events, videos_per_event=videos_per_event)

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
		videos = [v.url for v in get_videos_for_event(title)]

	return render_template('event_page.html', title=title, page_exists=page_exists,
		parent_categories=parent_categories, videos=videos)

''' ************************************
	VIEW SCRAPED VIDEOS (SSSSHHHHHH)
	************************************'''
@application.route('/reddit_videos/<league>', methods=['GET'])
@login_required
@roles_accepted('admin')
def reddit_videos(league):
	if league == None:
		return redirect(url_for('reddit_videos', league="nfl"))
	
	supported_leagues = ["baseball", "nfl"]
	posts = None
	league = league.lower()

	# change mlb to baseball (internally)
	if league == "mlb":
		league = "baseball"

	# check to see if there are params for days to look back
	days_back = 2
	if request.args.get('days_back') != None:
		days_back = int(request.args.get('days_back'))

	if league in supported_leagues:
		# get last 24 hours
		posts = Videopost.query.filter_by(league=league).\
			filter(Videopost.date_posted > datetime.utcnow() - timedelta(days=days_back)).\
			order_by(Videopost.date_posted).all()

	return render_template('reddit_videos.html', posts=posts, league=league)

''' ************************************
	HELPER FUNCTIONS
	************************************'''

def get_parent_cats_for_page(title):
	return LinkToCategory.query.filter_by(title_from=title).all()

# gets subcategories for a category
def get_subcats_for_cat(title):
	return Category.query.join(LinkToCategory, Category.title==LinkToCategory.title_from).\
		filter_by(namespace_from="category", title_to=title).all()

# gets events to report UP to a category
def get_events_for_cat(title):
	return Event.query.join(LinkToCategory, Event.title==LinkToCategory.title_from).\
		filter_by(namespace_from="event", title_to=title).all()

def get_nested_events_for_cat(cat_root):
	events_set = set()				# the set we return
	stack_unvisited = []			# stack of unvisited categories in BFS
	visited = defaultdict(bool)		# hashmap of visited entries

	stack_unvisited.append(cat_root)

	# start breadth-first search for all nested events
	while len(stack_unvisited) > 0:
		cat = stack_unvisited.pop()
		visited[cat] = True

		# add unvisited subcategories to stack_unvisited
		subcats = get_subcats_for_cat(cat.title)
		for subcat in subcats:
			if not visited[subcat]:
				stack_unvisited.append(subcat)

		# add events to set
		events = get_events_for_cat(cat.title)
		for event in events:
			events_set.add(event)

	return events_set

def get_videos_for_event(title):
	return VideoLinkToEvent.query.\
		join(Video, VideoLinkToEvent.video_from==Video.id).\
		join(VideoTextRevision, Video.latest_title_id==VideoTextRevision.text_id).\
		join(Text, VideoTextRevision.text_id==Text.id).\
		join(Event, VideoLinkToEvent.event_to==Event.id).filter_by(title=title).\
		add_columns(Video.url, Video.posted_by, Text.text).all()
