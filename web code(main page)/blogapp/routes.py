from flask import render_template, flash, redirect, url_for, session,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp import app, db
from blogapp.forms import LoginForm, SignupForm
from blogapp.models import User
from blogapp.config import Config
import os

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'User'}
	return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user_in_db = User.query.filter(User.username == form.username.data).first()
		if not user_in_db:
			flash('No user found with username: {}'.format(form.username.data))
			return redirect(url_for('login'))
		if (check_password_hash(user_in_db.password_hash, form.password.data)):
			flash('Login success!')
			session["USERNAME"] = user_in_db.username
			return redirect(url_for('customer_index'))
		flash('Incorrect Password')
		return redirect(url_for('login'))
	return render_template('login.html', title='Sign in', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		if form.password.data != form.password2.data:
			flash('Passwords do not match!')
			return redirect(url_for('signup'))
		user_in_db = User.query.filter(User.username == form.username.data).first()
		if user_in_db:
			flash('Username already existed!')
			return redirect(url_for('signup'))
		passw_hash = generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
		db.session.add(user)
		db.session.commit()
		flash('User registered with username:{}'.format(form.username.data))
		session["USERNAME"] = user.username
		return redirect(url_for('login'))
	return render_template('signup.html', title='Register a new user', form=form)

@app.route('/checkuser', methods=['POST'])
def check_username():
	chosen_name = request.form['username']
	user_in_db = User.query.filter(User.username == chosen_name).first()
	if not user_in_db:
		return jsonify({'text': 'Username is available',
						'returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! Username is already taken',
						'returvalue': 1})
	
@app.route('/checkemail', methods=['POST'])
def check_email():
	chosen_email = request.form['email']
	user_in_db = User.query.filter(User.email == chosen_email).first()
	if not user_in_db:
		return jsonify({'text': 'Email is available',
						'returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! Email is already taken',
						'returvalue': 1})

@app.route('/customer_index')
def customer_index():
	user = {'username': 'User'}
	return render_template('customer_index.html', title='Home', user=user)

