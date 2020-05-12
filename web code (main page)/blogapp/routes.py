from flask import render_template, flash, redirect, url_for, session,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp import app, db
from blogapp.forms import LoginForm, ERForm, CRForm, PetAccountForm, CustomerAccountForm, REForm, RSForm, PetAddForm, CustomerPasswordForm, PetDeleteForm, PostForm, PostForm2
from blogapp.models import Customer, Employee, Pet, Appointment, Post
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
		place=''
		if form.key.data=='BJ001':
			place='Beijing'
		if form.key.data=='SH002':
			place='Shanghai'
		if form.key.data=='CD003':
			place='Chengdu'
		user = Employee(username=form.username.data, key=place, password_hash=passw_hash)
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
	if not session.get("USERNAME") is None:
		return render_template('customer_index.html', title='Home', user=user)
	else:
		flash("User needs to either login or sign up")
		return redirect(url_for('index'))


@app.route('/customer_account', methods=['GET','POST'])
def customer_account():
	user = {'username': 'User'}
	form = CustomerAccountForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			customer_in_db.firstname = form.firstname.data
			customer_in_db.lastname = form.lastname.data
			customer_in_db.email = form.email.data
			customer_in_db.phone = form.telephone.data
			db.session.commit()
			return redirect(url_for('customer_index'))
		else:
			stored_account = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			if not stored_account:
				return render_template('customer_account.html', title='Init your details', form=form)
			else:
				form.email.data = stored_account.email
				form.firstname.data = stored_account.firstname
				form.lastname.data = stored_account.lastname
				form.telephone.data = stored_account.phone
				return render_template('customer_account.html', title='Modify your details', form=form)
		return render_template('customer_account.html', title='pet', user=user, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/customer_password', methods=['GET', 'POST'])
def customer_password():
	user = {'username': 'User'}
	form = CustomerPasswordForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			if not (check_password_hash(customer_in_db.password_hash, form.password.data)):
				flash('Incorrect Password')
				return redirect(url_for('customer_password'))
			if form.password2.data != form.password3.data:
				flash('Passwords do not match!')
				return redirect(url_for('customer_password'))
			else:
				customer_in_db.password_hash = generate_password_hash(form.password2.data)
				db.session.commit()
				return redirect(url_for('customer_index'))
		return render_template('customer_password.html', title='pet', user=user, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/pet_change', methods=['GET','POST'])
def pet_change():
	user = {'username': 'User'}
	form = PetAccountForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			pet_in_db = Pet.query.filter(Pet.id == form.pet_id.data).first()
			pet_in_db.name = form.pet_name.data 
			pet_in_db.old = form.pet_age.data
			pet_in_db.gender = form.pet_gender.data
			pet_in_db.type = form.pet_type.data
			pet_in_db.customer_id = customer_in_db.id
			db.session.commit()
			return redirect(url_for('reservation_s'))
		return render_template('pet_change.html', title='pet', user=user, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/pet_account', methods=['GET','POST'])
def pet_account():
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = Pet.query.filter(Pet.customer_id == customer_in_db.id ).all()
		return render_template('pet_account.html', title='pet', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/pet_add', methods=['GET','POST'])
def pet_add():
	user = {'username': 'User'}
	form = PetAddForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			pet = Pet(name=form.pet_name.data, old=form.pet_age.data, gender=form.pet_gender.data, type=form.pet_type.data, customer_id=customer_in_db.id)
			db.session.add(pet)
			db.session.commit()
			return redirect(url_for('reservation_s'))
		return render_template('pet_add.html', title='reservation', user=user, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/pet_delete', methods=['GET', 'POST'])
def pet_delete():
	user = {'username': 'User'}
	form = PetDeleteForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			pet_in_db = Pet.query.filter(Pet.id == form.pet_id.data).first()
			Appointment.query.filter(Appointment.pet_id == form.pet_id.data).delete(synchronize_session=False)
			db.session.delete(pet_in_db)
			db.session.commit()
			return redirect(url_for('customer_index'))
		return render_template('pet_delete.html', title='pet', user=user, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/reservation_e', methods=['GET','POST'])
def reservation_e():
	user = {'username': 'User'}
	form = REForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			emergency_appointment = Appointment(type='Emergency', date=form.time.data , city=form.city.data, details=form.detail.data,  
				pet_id=form.pet_id.data, customer_id=customer_in_db.id)
			db.session.add(emergency_appointment)
			db.session.commit()
			return redirect(url_for('customer_index'))
		return render_template('reservation_e.html', title='reservation', user=user, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/reservation_s', methods=['GET','POST'])
def reservation_s():
	user = {'username': 'User'}
	form = RSForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			standard_appointment = Appointment(type='Standard', time=form.time.data, city=form.city.data, 
				details=form.detail.data, date=form.date.data, pet_id=form.pet_id.data, customer_id=customer_in_db.id)
			db.session.add(standard_appointment)
			db.session.commit()
			return redirect(url_for('customer_index'))
		return render_template('reservation_s.html', title='reservation', user=user, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_a', methods=['GET', 'POST'])
def status_a():
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		return render_template('status_a.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_e', methods=['GET', 'POST'])
def status_e():
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		return render_template('status_e.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_sur', methods=['GET', 'POST'])
def status_sur():
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		# prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		prev_posts = Appointment.query.filter(Appointment.status==4 ).all()
		return render_template('status_sur.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/record_a', methods=['GET', 'POST'])
def record_a():
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		return render_template('record_a.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/record_e', methods=['GET', 'POST'])
def record_e():
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		return render_template('record_e.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/record_o', methods=['GET', 'POST'])
def record_o():
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		# prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		prev_posts = Appointment.query.filter(Appointment.status==4 ).all()
		return render_template('record_o.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/employee_base', methods=['GET', 'POST'])
def employee_base():
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Customer, Appointment).filter(Customer.id == Appointment.customer_id ).all()
		return render_template('employee_c.html', title='calendar', prev_posts=prev_posts, employee_in_db=employee_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/employee_c', methods=['GET', 'POST'])
def employee_c():
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Customer, Appointment).filter(Customer.id == Appointment.customer_id ).all()
		return render_template('employee_c.html', title='calendar', prev_posts=prev_posts, employee_in_db=employee_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/employee_t', methods=['GET', 'POST'])
def employee_t():
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Customer, Appointment).filter(Customer.id == Appointment.customer_id ).all()
		return render_template('employee_t.html', title='table', prev_posts=prev_posts, employee_in_db=employee_in_db )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/customer_chatting', methods=['GET', 'POST'])
def customer_chatting():
	form = PostForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			body = form.postbody.data
			user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			post = Post(body=body, customer = user_in_db, name=session.get("USERNAME"))
			db.session.add(post)
			db.session.commit()
			return redirect(url_for('customer_chatting'))
		else:
			user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			prev_posts = Post.query.filter(Post.user_id == user_in_db.id).all()
			print("Checking for user: {} with id: {}".format(user_in_db.username, user_in_db.id))
			return render_template('customer_chatting.html', title='Message', prev_posts=prev_posts, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/employee_chatting', methods=['GET', 'POST'])
def employee_chatting():
	form = PostForm2()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			body = form.postbody.data
			who=form.who.data
			user_in_db = Customer.query.filter(Customer.username == who).first()
			if user_in_db:
				post = Post(body = body, customer = user_in_db, name=session.get("USERNAME"))
				db.session.add(post)
				db.session.commit()
			return redirect(url_for('employee_chatting'))
		else:
			# user_in_db = Customer.query.first()
			prev_posts = Post.query.all()
			# print("Checking for user: {} with id: {}".format(user_in_db.username, user_in_db.id))
			return render_template('employee_chatting.html', title='Message', prev_posts=prev_posts, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/logout')
def logout():
	session.pop("USERNAME", None)
	return redirect(url_for('login'))

@app.route('/detail')
def detail():
	user = {'username': 'User'}
	return render_template('detail.html', title='detail', user=user )