from app import application, db, models, forms, user_datastore, sample_data, security
from app.forms import RegistrationForm, CategorySubmissionForm, ChannelCreationForm, EventSubmissionForm, VideoSubmissionForm, UserRoleForm
from app.models import *
from flask import render_template, request, jsonify, flash, redirect, url_for, Markup
from flask_security import current_user, login_required, login_user, logout_user
from flask_security.utils import hash_password, verify_and_update_password
from flask_security.decorators import roles_required, roles_accepted
from datetime import datetime, timedelta
from sqlalchemy import desc
from collections import defaultdict
from werkzeug.datastructures import ImmutableMultiDict
import pytz
import json

application.jinja_env.globals['CHANNELS'] = Channel.query.join(Category, Channel.id_cat==Category.id).add_columns(Category.title).all()

# global array for all posts
VIDEOS_BUFFER = []

# class that holds buffer of reddit posts
class Videos():
	def __init__(self, category=None):
		self.videos = get_nested_videos_for_cat(category=category)
		self.index = 0

	def __iter__(self):
		return self

	def next(self):
		try:
			video = self.videos[self.index]
		except IndexError:
			raise StopIteration
		self.index += 1
		return video


def get_next_videos():
	videos = []
	for i in range(10):
		videos.append(VIDEOS_BUFFER.next())
	return videos

@application.route('/load-more/', methods=['GET'])
# @roles_accepted('admin', 'moderator', 'beta_user')
def load_more_videos():
    stop_iteration_hit = False
    posts = []

    try:
        posts = get_next_videos()
    except StopIteration:
        stop_iteration_hit = True
        
    return jsonify(result = {"posts": [{ "url": p.url,
										 "text": p.text,
										 "uploaded_at": p.uploaded_at}
										 # "is_reddit": True if 'reddit' in p.url else False } 
									for p in posts],
                             "error": stop_iteration_hit})



@application.route('/')
def home_page():
	videos = []
	# events = []
	# channels = Channel.query.join(Category, Category.id==Channel.id_cat).\
	# 	add_columns(Category.title).all()

	# for channel in channels:
	# 	# get all nested events
	# 	events.extend([event.title for event in get_nested_events_for_cat(channel, days_back=2)])
	
	# get videos from global buffer
	global VIDEOS_BUFFER
	VIDEOS_BUFFER = Videos()
	videos = get_next_videos()

	return render_template('home_page.html', videos=videos)

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

# nothing in login but the route still needs to be made!
@application.route('/login', methods=['GET', 'POST'])
def login():
	pass

@application.route('/register', methods=['GET', 'POST'])
# @roles_accepted('admin', 'moderator')						# DELETE THIS!
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home_page'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user_datastore.create_user(username=form.username.data, email=form.email.data,
				password=hash_password(form.password.data),
				firstname=form.firstname.data, lastname=form.lastname.data,
				created_at=datetime.utcnow(), login_count=0)
		db.session.commit()

		user = User.query.filter_by(username=form.username.data).all()
		if len(user) == 1 and user[0] != None:
			login_user(user[0])

		flash('You have successfully registered your account!')
		return redirect(url_for('home_page'))
	return render_template('security/register_user.html', title='Register', form=form)

@application.route('/load_sample_data', methods=['GET', 'POST'])
@roles_accepted('admin')
def load_sample_data():
	if current_user.id != None:
		sample_data.load(current_user.id)

	return render_template('home_page.html')


''' ************************************
	SETTINGS / ADMIN
	************************************'''
# admin page to view signed up users
@application.route('/settings/user_access')
@roles_accepted('admin')
def user_access():
	return render_template('user_access.html', users=User.query.all())

# admin page to change user roles
@application.route('/settings/user_access/<username>', methods=['GET', 'POST'])
@roles_accepted('admin')
def edit_user_roles(username):
	#  query for user
	user = User.query.filter_by(username=username).first()
	user = user_datastore.get_user(user.id)
	
	if request.method == 'POST':
		form = UserRoleForm()
		if form.validate_on_submit():
			roles = []

			# find roles
			beta_user = user_datastore.find_role('beta_user')
			scraper = user_datastore.find_role('scraper')
			moderator = user_datastore.find_role('moderator') 
			admin = user_datastore.find_role('admin')

			# check each selected parent category and add a link to the db
			if form.is_beta_user.data:# and not user.has_role(beta_user):
				user_datastore.add_role_to_user(user, beta_user)
			else:
				user_datastore.remove_role_from_user(user, beta_user)

			if form.is_scraper.data:# and not user.has_role(scraper):
				user_datastore.add_role_to_user(user, scraper)
			else:
				user_datastore.remove_role_from_user(user, scraper)

			if form.is_moderator.data:# and not user.has_role(moderator):
				user_datastore.add_role_to_user(user, moderator)
			else:
				user_datastore.remove_role_from_user(user, moderator)

			if form.is_admin.data:# and not user.has_role(admin):
				user_datastore.add_role_to_user(user, admin)
			else:
				user_datastore.remove_role_from_user(user, admin)

			db.session.commit()

			flash('User roles edited.')
	else:
		# adds params to form, if provided
		form = UserRoleForm()
	
	return render_template('edit_user_roles.html', form=form, user=user)

# user page
@application.route('/user/<username>')
@roles_accepted('admin', 'beta_user')
def user_page(username):
	return render_template('user_page.html', user=User.query.filter_by(username=username).first(),
		current_user=current_user)


''' ************************************
	PAGE CREATION
	************************************'''

# form to submit a new category
@application.route('/category_submission', methods=['GET', 'POST'])
@roles_accepted('admin', 'moderator', 'beta_user')
def category_submission():
	if request.method == 'POST':
		form = CategorySubmissionForm()
		if form.validate_on_submit():
			#  add new category to db
			category = Category(title=form.category_title.data, category_type=form.category_type.data,
				created_at=datetime.utcnow(), created_by=current_user.id)
			db.session.add(category)

			# iterate through each selected parent category and add a link to the db
			for cat in form.parent_category.data:
				categorylink = LinkToCategory(title_from=category.title, namespace_from="category",
					title_to=cat.title, created_at=datetime.utcnow(), created_by=current_user.id)
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
			channel = Channel(id_cat=form.category_for_channel.data.id, created_at=datetime.utcnow(),
				created_by=current_user.id)
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
			event_type = form.event_type.data
			event_title = form.event_title.data
			start_time = datetime.strptime("%s %s" % (form.start_time.data, form.tz.data), "%m/%d/%Y %I:%M %p %z")

			# create default type event WE'RE CURRENTLY SKIPPING THIS
			if event_type == "default":
				pass
				# end_time = datetime.strptime("%s %s" % (form.end_time.data, form.tz.data), "%m/%d/%Y %I:%M %p %z")

				# event = Event(title=event_title, start_time=start_time, end_time=end_time,
				# 	event_type=event_type, created_at=datetime.utcnow(), created_by=current_user.id)
				# db.session.add(event)
				
				# # iterate through each selected parent category and add a link to the db
				# for cat in form.parent_category.data:
				# 	categorylink = LinkToCategory(title_from=event.title, namespace_from="event",
				# 		title_to=cat.title, created_at=datetime.utcnow(), created_by=current_user.id)
				# 	db.session.add(categorylink)
			
			# create sports game type event
			else:
				league = form.league.data
				away_team = form.away_team.data.title
				home_team = form.home_team.data.title
				event_title = "%s at %s: %s" % (away_team, home_team,
					start_time.strftime("%b %-d, %Y"))

				# create event
				event = Event(title=event_title, start_time=start_time,	event_type=event_type,
					created_at=datetime.utcnow(), created_by=current_user.id)
				db.session.add(event)
				
				# make parent categories for both teams
				link_away_team = LinkToCategory(title_from=event.title, namespace_from="event",
					title_to=away_team, created_at=datetime.utcnow(), created_by=current_user.id)
				link_home_team = LinkToCategory(title_from=event.title, namespace_from="event",
					title_to=home_team, created_at=datetime.utcnow(), created_by=current_user.id)
				db.session.add(link_away_team)
				db.session.add(link_home_team)

			# db.session.commit()

			# redirect to newly created category
			flash('New event created!')

			# redirect back to video upload if redirect specified
			next_url = request.args.get('next_url')
			if next_url != None:
				return redirect(next_url)
			else:
				return redirect(url_for('event_page', page_title=event.title))
		else:
			print(form.errors)
	else:
		# adds params to form, if provided
		form = EventSubmissionForm(request.args)

	return render_template('event_submission.html', title='Event Submission', form=form)

# submit video
@application.route('/video_submission', methods=['GET', 'POST'])
@roles_accepted('admin', 'moderator')
def video_submission():
	queue = request.args.getlist('queue')
	video_date = request.args.get('video_date')		# date of video for video popped from queue

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
				width=-1, duration=-1, latest_title_id=text_rev.id, uploaded_at=datetime.utcnow())
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

			# redirect to next video to upload if queue not empty
			return redirect(url_for('video_submission_next', queue=queue))

			# return redirect(url_for('video_page', video_id=video.id))
			render_template('video_submission.html', title='Submit New Video', form=form)
	else:
		# adds params to form, if provided
		form = VideoSubmissionForm(request.args)
	return render_template('video_submission.html', title='Submit New Video', form=form,
		queue=queue, video_date=video_date)

# go to next video in queue for video submission
@application.route('/video_submission_next/', methods=['GET'])
@roles_accepted('admin', 'moderator')
def video_submission_next():
	queue = request.args.get('queue')

	# if there's no queue, don't pass along queue into request
	if queue == '[]' or queue == None:
		return redirect(url_for('reddit_videos'))

	# unpack json
	queue = json.loads(queue)

	# pop first video from queue for form
	video_data = Videopost.query.get(queue.pop())
	video_url = video_data.mp4_url
	video_title = video_data.title
	video_date = video_data.date_posted

	# convert queue back to json for call
	queue_json = json.dumps(queue)

	return redirect(url_for('video_submission', video_url=video_url, video_title=video_title,
		video_date=video_date, queue=queue_json))


''' ************************************
	PAGE MODIFICATION
	************************************'''
# modify event page
@application.route('/event/<page_title>/edit', methods=['GET', 'POST'])
@roles_accepted('admin', 'moderator')
def edit_event_page(page_title):
	# get event from title
	event_title = page_title.replace('_', ' ')
	event = Event.query.filter_by(title=event_title).first()

	if event != None:
		if request.method == 'POST':
			form = EventSubmissionForm()
			if form.validate_on_submit():
				#  modify changed teams
				teams_new = set([form.away_team.data, form.home_team.data])
				teams_old = set(get_teams_for_event(event.title))

				teams_to_add = teams_new.difference(teams_old)
				teams_to_remove = teams_old.difference(teams_new)

				# remove links to event for teams no longer in event
				for t in teams_to_remove:
					link = LinkToCategory.query.filter_by(title_from=event.title, title_to=t.title, namespace_from='event').first()
					db.session.delete(link)

				# add links to event for new team additions
				for t in teams_to_add:
					link = LinkToCategory(title_from=event.title, title_to=t.title, namespace_from='event',
						created_at=datetime.utcnow(), created_by=current_user.id)
					db.session.add(link)

				away_team = form.away_team.data.title
				home_team = form.home_team.data.title
				start_time = datetime.strptime("%s %s" % (form.start_time.data, form.tz.data), "%m/%d/%Y %I:%M %p %z")
				event_title = "%s at %s: %s" % (away_team, home_team, start_time.strftime("%b %-d, %Y"))

				# change start time or title, if necessary
				if start_time != event.start_time or event_title != event.title:
					event_new = Event(id=event.id, title=event_title, start_time=start_time)
					db.session.merge(event_new)

				db.session.commit()
				flash('Event successfully edited.')
				return redirect(url_for('event_page', page_title=event.title))

		else:
			# find home and away teams from event title
			teams = get_teams_for_event(event.title)

			start_time_utc = event.start_time.astimezone(pytz.utc)

			# args = urllib.parse.urlencode({
			args = ImmutableMultiDict([
				('event_type', 'sports_game'),
				('league', str(find_league_for_event(event.title).id)),
				('event_title', event.title),
				('away_team', str(teams[0].id)),
				('home_team', str(teams[1].id))
				# ('start_time', str(start_time_utc))
			])

			form = EventSubmissionForm(args)
			return render_template('event_submission.html', title='Edit Event', form=form,
				event=event, edit_event=True, start_time_val=str(start_time_utc))
	else:
		flash('Event not found!')
		return redirect(url_for('home_page'))
	
	# return same template from event page submission, with new parameter for editing a current event



''' ************************************
	PAGE VIEWS
	************************************'''

# view for category page
@application.route('/category/<page_title>/', methods=['GET'])
@roles_accepted('admin', 'moderator', 'beta_user')
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
# @application.route('/<page_title>/', methods=['GET'])
@roles_accepted('admin', 'moderator', 'beta_user')
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
		events = [event.title for event in get_nested_events_for_cat(category_page, days_back=2)]

		# get all videos, sorted by upload time
		videos = get_nested_videos_for_cat(category_page)

		return render_template('channel_page.html', title=title, parent_categories=parent_categories,
			subcategories=subcategories, events=events, videos=videos)

# view all events for a channel
@application.route('/channel/<page_title>/events', methods=['GET'])
@application.route('/<page_title>/events', methods=['GET'])
@roles_accepted('admin', 'moderator', 'beta_user')
def channel_page_events(page_title):
	# redirect if url has spaces (we convert them to underscores for friendlier urls)
	if ' ' in page_title:
		return redirect(url_for('channel_page', page_title=page_title.replace(' ', '_')))

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

		# get all nested events
		events = [event.title for event in get_nested_events_for_cat(category_page)]

		return render_template('channel_page_events.html', title=title, events=events)

# view for category page
@application.route('/event/<page_title>/', methods=['GET'])
@roles_accepted('admin', 'moderator', 'beta_user')
def event_page(page_title):
	# redirect if url has spaces (we convert them to underscores for friendlier urls)
	if ' ' in page_title:
		return redirect(url_for('event_page', page_title=page_title.replace(' ', '_')))

	page_exists = False 					# boolean used to track if the category page exsits
	parent_categories = []					# array used to track parent categories for the queried category
	subcategories = []
	videos = []
	title = page_title.replace('_', ' ')	# replace underscores with spaces
	event_page = Event.query.filter_by(title=title).first()

	if event_page is not None:
		page_exists = True
		
		title = event_page.title 	# fixes any capitalization errors

		# get parent categories
		parent_categories = [link.title_to for link in get_parent_cats_for_page(title)]

		# get all videos
		videos = [v for v in get_videos_for_event(title)]

	return render_template('event_page.html', title=title, page_exists=page_exists,
		parent_categories=parent_categories, videos=videos)

# video page
@application.route('/video/<video_id>/', methods=['GET'])
@roles_accepted('admin', 'moderator', 'beta_user')
def video_page(video_id):
	video = None
	is_reddit = True if 'reddit' in video_id else False

	if is_reddit:
		video = db.session.\
				query(Videopost.title.label('text'), Videopost.mp4_url.label('url'),
					Videopost.date_posted.label('uploaded_at')).filter_by(id=video_id).first()
	else:
		video = Video.query.\
				join(VideoTextRevision, Video.latest_title_id==VideoTextRevision.text_id).\
				join(Text, VideoTextRevision.text_id==Text.id).\
				filter_by(id=video_id).add_columns(Video.url, Text.text).first()
	events = get_events_for_video(video_id)
	return render_template('video_page.html', video=video, events=events)


''' ************************************
	VIEW SCRAPED VIDEOS (SSSSHHHHHH)
	************************************'''
@application.route('/reddit_videos/<league>', methods=['GET', 'POST'])
@application.route('/reddit_videos', methods=['GET', 'POSaT'])
@login_required
@roles_accepted('admin', 'scraper')
def reddit_videos(league='mlb'):
	if request.method == 'POST':
		# get list of all videos to post to event, and reverse them so oldest videos appear first
		videos_to_upload = list(reversed(request.form.getlist('video_upload')))

		# make get request back to reddit_videos if no video selected
		if len(videos_to_upload) == 0:
			flash('No video selected!')
			return redirect(url_for('reddit_videos', league=league))

		queue_json = json.dumps(videos_to_upload)

		return redirect(url_for('video_submission_next', queue=queue_json))
	else:		
		supported_leagues = ["baseball", "nfl", "nba"]
		posts_filted = None
		league = league.lower()

		# change mlb to baseball (internally)
		if league == "mlb":
			league = "baseball"

		# check to see if there are params for days to look back
		days_back = 1
		if request.args.get('days_back') != None:
			days_back = int(request.args.get('days_back'))

		if league in supported_leagues:
			posts_filtered = []

			# get last n days of reddit
			posts_reddit = Videopost.query.filter_by(league=league).\
				filter(Videopost.date_posted > datetime.utcnow() - timedelta(days=days_back)).\
				order_by(Videopost.date_posted).all()

			# get all posts from lob (so we know which to remove from feed)
			urls = [v.url for v in Video.query.all()]

			# super inefficient call to remove already uploaded videos
			for p in posts_reddit:
				if p.mp4_url not in urls:
					posts_filtered.append(p)

		return render_template('reddit_videos.html', posts=posts_filtered, league=league)

''' ************************************
	HELPER FUNCTIONS
	************************************'''

def get_parent_cats_for_page(title):
	return LinkToCategory.query.filter_by(title_from=title).order_by(LinkToCategory.title_from).all()

# gets subcategories for a category
def get_subcats_for_cat(title):
	return Category.query.join(LinkToCategory, Category.title==LinkToCategory.title_from).\
		filter_by(namespace_from="category", title_to=title).order_by(Category.title).all()

# gets events to report UP to a category
def get_events_for_cat(title, days_back=None):
	if days_back == None:
		return Event.query.join(LinkToCategory, Event.title==LinkToCategory.title_from).\
			filter_by(namespace_from="event", title_to=title).\
			order_by(desc(Event.start_time)).all()
	else:
		return Event.query.join(LinkToCategory, Event.title==LinkToCategory.title_from).\
			filter_by(namespace_from="event", title_to=title).\
			filter(Event.start_time > datetime.utcnow() - timedelta(days=days_back)).\
			order_by(desc(Event.start_time)).all()

def get_nested_events_for_cat(cat_root, days_back=None):
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
		events = get_events_for_cat(cat.title, days_back)
		for event in events:
			events_set.add(event)

	# return sorted sets
	return sorted(events_set, key=lambda x: x.start_time, reverse=True)

def get_videos_for_event(title):
	return VideoLinkToEvent.query.\
		join(Video, VideoLinkToEvent.video_from==Video.id).\
		join(VideoTextRevision, Video.latest_title_id==VideoTextRevision.text_id).\
		join(Text, VideoTextRevision.text_id==Text.id).\
		join(Event, VideoLinkToEvent.event_to==Event.id).filter_by(title=title).\
		add_columns(Video.url, Video.id, Video.posted_by, Video.uploaded_at,
			Text.text, Event.title).all()

# gets videos for all nested videos in category
def get_nested_videos_for_cat(category=None, page=None):
	# page size for pagination
	page_size = 10
	channels = [category]
	videos_all = []
	matching_subreddit = None
	
	# set default pagination if user inputs None
	if page == None:
		page = 1
	
	# if no category is specified, search all channels (home page functionality)
	if category == None:
		channels = Channel.query.join(Category, Category.id==Channel.id_cat).\
							add_columns(Category.title).all()
	
	# get all videos for each channel we're parsing
	for channel in channels:
		videos_tagged = []
		events = get_nested_events_for_cat(channel)

		# get all videos tagged in our system
		for event in events:
			videos_tagged.extend(get_videos_for_event(event.title))
		videos_all.extend(videos_tagged)

		# find subreddit to use for get untagged videos from reddit
		if channel.title == "NBA" or channel.title == "NFL":
			matching_subreddit = channel.title.lower()
		elif channel.title == "MLB":
			matching_subreddit = "baseball"

		# get untagged reddit videos, if category is applicable
		if matching_subreddit != None:
			videos_reddit = db.session.\
				query(Videopost.title.label('text'), Videopost.mp4_url.label('url'),
					Videopost.date_posted.label('uploaded_at'), Videopost.id).\
				filter_by(league=matching_subreddit).all()
			urls_tagged = [v.url for v in videos_tagged]

			for v in videos_reddit:
				if v.url not in urls_tagged:
					videos_all.append(v)

	videos_sorted = sorted(videos_all, key=lambda v: v.uploaded_at, reverse=True)#[page_size * (page - 1):page_size * page]
	return videos_sorted

# get teams for league
def get_teams_for_league(league):
	links =  LinkToCategory.query.\
		join(Category, Category.title==LinkToCategory.title_to).\
		filter_by(title="%s Teams" % league).order_by(LinkToCategory.title_from).all()

	return [Category.query.filter_by(title=link.title_from).first() for link in links]

# finds league given a team
def find_league_for_event(event_title):
	# get all leagues
	leagues = Category.query.filter_by(category_type="sports_league").all()
	event_teams = [t.title for t in get_teams_for_event(event_title)]

	# search for team match within all leagues
	for league in leagues:
		teams = [link.title_from for link in LinkToCategory.query.filter_by(title_to="%s Teams" % league.title)]
		if event_teams[0] in teams:
			return league

	return None

# finds teams in event title
def get_teams_for_event(event_title):
	s1 = event_title.split(':')[0]
	s2 = s1.split(' at ')
	return [Category.query.filter_by(title=team).all()[0] for team in s2]

# gets all linked events for a video
def get_events_for_video(video_id):
	return VideoLinkToEvent.query.filter_by(video_from=video_id).\
		join(Event, VideoLinkToEvent.event_to==Event.id).all()

