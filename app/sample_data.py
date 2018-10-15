from app import db, models
from app.models import *
from datetime import datetime


TEAMS_MLB = [
	"Los Angeles Dodgers",
	"Milwaukee Brewers",
	"Boston Red Sox",
	"Houston Astros"
]

def load(user_id):
# load sample data (if not already loaded)
	if len(Category.query.all()) == 0:
		sports_cat = Category(created_by=user_id, title="Sports", category_type="default", created_at=datetime.utcnow())
		db.session.add(sports_cat)
		
		setup_sport("MLB", user_id)

		db.session.commit()

def setup_sport(league, user_id):
	teams = []
	sport = ""

	if league == "MLB":
		sport = "Baseball"
		teams = TEAMS_MLB
	else:
		return

	# add parent categories
	sport_cat = Category(created_by=user_id, title="%s" % sport, category_type="default", created_at=datetime.utcnow())
	league_cat = Category(created_by=user_id, title="%s" % league, category_type="sports_league", created_at=datetime.utcnow())
	season_cat = Category(created_by=user_id, title="%s Teams" % league, category_type="default", created_at=datetime.utcnow())
	link1 = LinkToCategory(created_by=user_id, title_from="%s" % sport, namespace_from="category", title_to="Sports", created_at=datetime.utcnow())
	link2 = LinkToCategory(created_by=user_id, title_from="%s" % league, namespace_from="category", title_to="%s" % sport, created_at=datetime.utcnow())
	link3 = LinkToCategory(created_by=user_id, title_from="%s Teams" % league, namespace_from="category", title_to="%s" % league, created_at=datetime.utcnow())

	db.session.add(sport_cat)
	db.session.add(league_cat)
	db.session.add(season_cat)
	db.session.add(link1)
	db.session.add(link2)
	db.session.add(link3)
	db.session.flush()				# update primary keys

	channel = Channel(created_by=user_id, id_cat=league_cat.id, created_at=datetime.utcnow())
	db.session.add(channel)

	# add teams
	for team in teams:
		cat = Category(created_by=user_id, title=team, category_type="sports_team", created_at=datetime.utcnow())
		link = LinkToCategory(created_by=user_id, title_from=team, namespace_from="category", title_to="%s Teams" % league, created_at=datetime.utcnow())
		db.session.add(cat)
		db.session.add(link)

