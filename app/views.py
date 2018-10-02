from app import application, db, models, forms, user_datastore#, login_manager
from app.forms import LoginForm, RegistrationForm
from app.models import *
from flask import render_template, request, jsonify, flash, redirect, url_for, Markup
from flask_security import current_user, login_user, login_required, logout_user
from flask_security.utils import hash_password, verify_and_update_password
from datetime import datetime
from sqlalchemy import desc
import json


@application.login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

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
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_datastore.create_user(username=form.username.data, email=form.email.data,
        			password=hash_password(form.password.data),
        			# password=form.password.data,
        			firstname=form.firstname.data, lastname=form.lastname.data,
        			created_at=datetime.utcnow(), login_count=0)

        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('home_page'))
    return render_template('register.html', title='Register', form=form)

@application.route('/')
def home_page():
	return render_template('index.html')