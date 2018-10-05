from app import application, db, models, forms, user_datastore#, login_manager
from app.forms import LoginForm, RegistrationForm, CategorySubmissionForm
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
	CATEGORIES
	************************************'''

# form to submit a new category
@application.route('/category_submission', methods=['GET', 'POST'])
@roles_accepted('admin', 'moderator')
def category_submission():
	if request.method == 'POST':
		form = CategorySubmissionForm()
		if form.validate_on_submit():
			page = Page(namespace='category', title=form.category_title.data, created_at=datetime.utcnow())
			db.session.add(page)
			db.session.commit()		# must first commit and flush page to fix foreign key constraint issue on categorylink
			db.session.flush()

			categorylink = CategoryLink(id_from=Page.query.filter_by(title=page.title).first().id, id_to=form.parent_category.data, created_at=datetime.utcnow())
			db.session.add(categorylink)
			db.session.commit()
			
			# redirect to newly created category
			flash('New category created!')
			return redirect(url_for('category_page', page_title=page.title))
	else:
		# adds params to form, if provided
		form = CategorySubmissionForm(request.args)
	return render_template('category_submission.html', title='Submit New Category', form=form)

# view for category page
@application.route('/category/<page_title>/', methods=['GET'])
def category_page(page_title):
	# redirect if url has spaces (we convert them to underscores for friendlier urls)
	if ' ' in page_title:
		return redirect(url_for('category_page', page_title=page_title.replace(' ', '_')))

	page_exists = False 					# boolean used to track if the category page exsits
	parent_categories = []					# array used to track parent categories for the queried category
	subcategories = []
	title = page_title.replace('_', ' ')	# replace underscores with spaces
	page = Page.query.filter_by(title=title).first()
	
	if page is not None:
		page_exists = True
		title = page.title 	# fixes any capitalization errors

		# get parent categories
		links_parent_categories = CategoryLink.query.filter_by(id_from=page.id).all()
		for link in links_parent_categories:
			parent_categories.append(Page.query.get(link.id_to).title)

		# get subcategories
		links_subcategories = CategoryLink.query.filter_by(id_to=page.id).all()
		for link in links_subcategories:
			subcategories.append(Page.query.get(link.id_from).title)

	return render_template('category_page.html', title=title, page_exists=page_exists,
		parent_categories=parent_categories, subcategories=subcategories)
