from app import application, db, models, forms, user_datastore, sample_data, security
from app.models import *
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, Markup, abort
from sqlalchemy import desc
import boto3
import json

api_v1 = Blueprint('api_v1', __name__)

# resource for posts
@api_v1.route('/posts', methods=['GET'])
def posts():
	channel = request.args.get('channel')
	sort = request.args.get('sort')
	page = int(request.args.get('page') or 1)		# the 'or 1' ensures we have some page number

	if sort == 'trending':
		return get_hot_posts()
	
	return get_posts_for_channel(channel, page)

# returns trending content
def get_hot_posts():
	dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
	table = dynamodb.Table('lobHotPostsByLeague')
	response = table.scan()
	data = response['Items']
	data_json = {}

	# convert all decimals to floats so the data becomes json serializable
	for i, league_data in enumerate(data):
		league = league_data['league']
		data_json[league] = []
		for j, post_data in enumerate(league_data['posts']):
			# update json with serializable attributes
			post_data['hot_score'] = float(post_data['hot_score'])
			post_data['width'] = int(post_data['width'])
			post_data['height'] = int(post_data['height'])
			post_data['reddit_score'] = int(post_data['reddit_score'])
			post_data['date_posted'] = datetime.strptime(post_data['date_posted'], "%Y-%m-%d %H:%M:%S")
			data_json[league].append(post_data)

	return jsonify(results=data_json)

# posts sorted by date per inputted channels
def get_posts_for_channel(channel, page):
	posts_serialized = []

	if channel == None:
		abort(400)

	if channel != None:
		posts = Videopost.query.filter_by(league=channel).order_by(desc(Videopost.date_posted)).paginate(page=page, per_page=10).items
		posts_serialized = [p.serialize for p in posts]

	return jsonify(results=posts_serialized)