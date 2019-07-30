from app import application, db, models, forms, user_datastore, sample_data, security
from app.api import common
from app.models import *
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, Markup, abort
from sqlalchemy import desc
import boto3
import json

api_v0 = Blueprint('api_v0', __name__)

# gets data for "hot" posts
@api_v0.route('/hot_posts', methods=['GET'])
def hot_posts():
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

@api_v0.route('/new/<sport>')
@api_v0.route('/new/')
@api_v0.route('/new')
def get_new_posts(sport=None):
	posts_serialized = []
	if sport != None:
		posts = Videopost.query.filter_by(league=sport).order_by(desc(Videopost.date_posted)).all()
		posts_serialized = [p.serialize for p in posts]
	# else default to nba
	else:
		posts = Videopost.query.filter_by(league="nba").order_by(desc(Videopost.date_posted)).all()
		posts_serialized = [p.serialize for p in posts]
	return jsonify(results=posts_serialized)