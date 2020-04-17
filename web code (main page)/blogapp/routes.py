from flask import render_template, flash, redirect, url_for, session,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp import app, db
from blogapp.forms import LoginForm, ERForm, CRForm, PetAccountForm, CustomerAccountForm, REForm, RSForm, PetAddForm
from blogapp.models import Customer, Employee
from blogapp.config import Config
import os

@app.route('/')
@app.route('/index')
def index():
	# user = {'username': 'User'}
	return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		customer_in_db = Customer.query.filter(Customer.username == form.username.data).first()
		employee_in_db = Employee.query.filter(Employee.username == form.username.data).first()
		if not customer_in_db and not employee_in_db:
			flash('No user found with username: {}'.format(form.username.data))
			return redirect(url_for('login'))
		elif employee_in_db and not customer_in_db:
			if (check_password_hash(employee_in_db.password_hash, form.password.data)):
				# flash('Login success!')
				session["USERNAME"] = employee_in_db.username
				return redirect(url_for('employee_base'))
			else:
				flash('Incorrect Password')
				return redirect(url_for('login'))
		elif customer_in_db and not employee_in_db:
			if (check_password_hash(customer_in_db.password_hash, form.password.data)):
				# flash('Login success!')
				session["USERNAME"] = customer_in_db.username
				return redirect(url_for('customer_index'))
			else:
				flash('Incorrect Password')
				return redirect(url_for('login'))
	return render_template('login.html', title='Sign in', form=form)

@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
	form = CRForm()
	if form.validate_on_submit():
		if form.password.data != form.password2.data:
			flash('Passwords do not match!')
			return redirect(url_for('customer_register'))
		user_in_db = Customer.query.filter(Customer.username == form.username.data).first()
		if user_in_db:
			flash('Username already existed!')
			return redirect(url_for('customer_register'))
		passw_hash = generate_password_hash(form.password.data)
		user = Customer(username=form.username.data, email=form.email.data, password_hash=passw_hash)
		db.session.add(user)
		db.session.commit()
		flash('User registered with username:{}'.format(form.username.data))
		session["USERNAME"] = user.username
		return redirect(url_for('login'))
	return render_template('customer_register.html', title='Register a new user', form=form)

@app.route('/employee_register', methods=['GET', 'POST'])
def employee_register():
	form = ERForm()
	if form.validate_on_submit():
		if form.password.data != form.password2.data:
			flash('Passwords do not match!')
			return redirect(url_for('employee_register'))
		user_in_db = Employee.query.filter(Employee.username == form.username.data).first()
		if user_in_db:
			flash('Username already existed!')
			return redirect(url_for('employee_register'))
		passw_hash = generate_password_hash(form.password.data)
		user = Employee(username=form.username.data, key=form.key.data, password_hash=passw_hash)
		db.session.add(user)
		db.session.commit()
		flash('User registered with username:{}'.format(form.username.data))
		session["USERNAME"] = user.username
		return redirect(url_for('login'))
	return render_template('employee_register.html', title='Register a new employee', form=form)

@app.route('/checkuser', methods=['POST'])
def check_username():
	chosen_name = request.form['username']
	customer_in_db = Customer.query.filter(Customer.username == chosen_name).first()
	employee_in_db = Employee.query.filter(Employee.username == chosen_name).first()
	if not customer_in_db and not employee_in_db:
		return jsonify({'text': 'Username is available',
						'returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! Username is already taken',
						'returnvalue': 1})
	
@app.route('/checkemail', methods=['POST'])
def check_email():
	chosen_email = request.form['email']
	user_in_db = Customer.query.filter(Customer.email == chosen_email).first()
	if not user_in_db:
		return jsonify({'text': 'Email is available',
						'returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! Email is already taken',
						'returnvalue': 1})

@app.route('/customer_index', methods=['GET','POST'])
def customer_index():
	user = {'username': 'User'}
	return render_template('customer_index.html', title='Home', user=user)

@app.route('/customer_account', methods=['GET','POST'])
def customer_account():
	user = {'username': 'User'}
	form = CustomerAccountForm()
	return render_template('customer_account.html', title='account', user=user, form=form)

@app.route('/pet_account', methods=['GET','POST'])
def pet_account():
	user = {'username': 'User'}
	form = PetAccountForm()
	return render_template('pet_account.html', title='account', user=user, form=form)

@app.route('/record_a')
def record_a():
	user = {'username': 'User'}
	return render_template('record_a.html', title='record', user=user)

@app.route('/record_e')
def record_e():
	user = {'username': 'User'}
	return render_template('record_e.html', title='record', user=user)

@app.route('/reservation_e', methods=['GET','POST'])
def reservation_e():
	user = {'username': 'User'}
	form = REForm()
	return render_template('reservation_e.html', title='reservation', user=user, form=form)

@app.route('/reservation_s', methods=['GET','POST'])
def reservation_s():
	user = {'username': 'User'}
	form = RSForm()
	return render_template('reservation_s.html', title='reservation', user=user, form=form)

@app.route('/status_a')
def status_a():
	user = {'username': 'User'}
	return render_template('status_a.html', title='status', user=user)

@app.route('/status_e')
def status_e():
	user = {'username': 'User'}
	return render_template('status_e.html', title='status', user=user)

@app.route('/status_sur')
def status_sur():
	user = {'username': 'User'}
	return render_template('status_sur.html', title='status', user=user)

@app.route('/pet_add', methods=['GET','POST'])
def pet_add():
	user = {'username': 'User'}
	form = PetAddForm()
	return render_template('pet_add.html', title='pet', user=user, form=form)

@app.route('/employee_base')
def employee_base():
	return render_template('employee_base.html', title='employee')

@app.route('/employee_index')
def employee_index():
	return render_template('employee_index.html', title='employee')


