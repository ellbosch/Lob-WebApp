from app import application, login_manager, db, models, forms#, reddit
from app.forms import LoginForm, RegistrationForm
from app.models import *
from flask import render_template, request, jsonify, flash, redirect, url_for, Markup
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from datetime import datetime
from sqlalchemy import desc
import json


@login_manager.user_loader
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
        if user is None or not user.check_password(form.password.data):
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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('home_page'))
    return render_template('register.html', title='Register', form=form)

@application.route('/')
def home_page():
	return render_template('index.html')