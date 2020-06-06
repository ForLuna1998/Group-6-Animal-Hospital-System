from flask import render_template, flash, redirect, url_for, session,request,jsonify,json
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp import app, db
from blogapp.forms import LoginForm, ERForm, CRForm, PetAccountForm, CustomerAccountForm, CustomerPasswordForm, PetChangeForm,PostForm, ManageForm
from blogapp.models import Customer, Employee, Pet, Appointment, Post
from blogapp.config import Config
from blogapp.locales_cn import cn
from blogapp.locales_en import en
import os

current_path = ""

language={
	'en': en,
	'cn': cn
}

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'User'}
	session['current_path'] = request.path
	return render_template('index.html', title='Home', user=user, language=language[render_languages()])


@app.route('/login', methods=['GET', 'POST'])
def login():
	session['current_path'] = request.path
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
				return redirect(url_for('employee_f'))
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
	return render_template('login.html', title='Sign in', form=form, language=language[render_languages()])


@app.route('/customer_base', methods=['GET', 'POST'])
def customer_base():
	session['current_path'] = request.path
	session['current_patth']=request.path
	return render_template('customer_base.html', language=language[render_languages()])


@app.route('/customer_base_a', methods=['GET', 'POST'])
def customer_base_a():
	session['current_path'] = request.path
	session['current_patth']=request.path
	return render_template('customer_base_a.html', language=language[render_languages()])



@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
	session['current_path'] = request.path
	form = CRForm()
	if form.validate_on_submit():
		if form.password.data != form.password2.data:
			flash('Passwords do not match!')
			return redirect(url_for('customer_register'))
		passw_hash = generate_password_hash(form.password.data)
		if form.username.data=='Employee123':
			user = Employee(username=form.username.data, key='Beijing', password_hash=passw_hash)
			db.session.add(user)
			db.session.commit()
		else:
			user = Customer(username=form.username.data, email=form.email.data, password_hash=passw_hash)
			db.session.add(user)
			db.session.commit()
		flash('User registered with username:{}'.format(form.username.data))
		session["USERNAME"] = user.username
		return redirect(url_for('login'))
	return render_template('customer_register.html', title='Register a new user', form=form, language=language[render_languages()])


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
		return jsonify({'text': 'Email is available','returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! Email is already taken','returnvalue': 1})


@app.route('/checkpassword', methods=['POST'])
def check_password():
	chosen_password=request.form['password']
	return jsonify({'text': 'Password is available'})


@app.route('/checkkey', methods=['POST'])
def check_key():
	chosen_key = request.form['k']
	if chosen_key == 'BJ001' or chosen_key == 'SH002' or chosen_key == 'CD003':
		return jsonify({'text': 'Key is valid', 'returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! You should enter the right key', 'returnvalue': 1})


@app.route('/customer_index', methods=['GET','POST'])
def customer_index():
	session['current_path'] = request.path
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			username = session.get("USERNAME")
			return render_template('customer_index.html', title='Home', user=user, username=username, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		return redirect(url_for('index'))


@app.route('/customer_account', methods=['GET','POST'])
def customer_account():
	session['current_path'] = request.path
	user = {'username': 'User'}
	form = CustomerAccountForm()
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
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
					return render_template('customer_account.html', title='customer', username=username, form=form, language=language[render_languages()])
				else:
					form.email.data = stored_account.email
					form.firstname.data = stored_account.firstname
					form.lastname.data = stored_account.lastname
					form.telephone.data = stored_account.phone
					return render_template('customer_account.html', title='Modify your details', username=username, form=form, language=language[render_languages()])
			return render_template('customer_account.html', title='account', user=user, username=username, form=form, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/customer_password', methods=['GET', 'POST'])
def customer_password():
	session['current_path'] = request.path
	user = {'username': 'User'}
	form = CustomerPasswordForm()
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			if form.validate_on_submit():
				customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
				if not (check_password_hash(customer_in_db.password_hash, form.password3.data)):
					flash('Incorrect Password')
					return redirect(url_for('customer_password'))
				if form.password.data != form.password2.data:
					flash('Passwords do not match!')
					return redirect(url_for('customer_password'))
				else:
					customer_in_db.password_hash = generate_password_hash(form.password.data)
					db.session.commit()
					return redirect(url_for('customer_index'))
			return render_template('customer_password.html', title='password', user=user, username=username, form=form, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/pet_change', methods=['GET','POST'])
def pet_change():
	session['current_path'] = request.path
	user = {'username': 'User'}
	form = PetChangeForm()
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			petid = request.args.get("id")
			if form.validate_on_submit():
				customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
				pet_in_db = Pet.query.filter(Pet.id == petid).first()
				pet_in_db.name = form.pet_name.data 
				pet_in_db.old = form.pet_age.data
				pet_in_db.gender = form.pet_gender.data
				pet_in_db.type = form.pet_type.data
				pet_in_db.customer_id = customer_in_db.id
				db.session.commit()
				return redirect(url_for('pet_account'))
			else:
				stored_account = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
				stored_Paccount = Pet.query.filter(Pet.customer_id == stored_account.id, Pet.id == petid).first()
				if not stored_account:
					return render_template('pet_change.html', username=username, title='Init your details', form=form, language=language[render_languages()])
				else:
					form.pet_name.data = stored_Paccount.name
					form.pet_age.data = stored_Paccount.old
					form.pet_gender.data = stored_Paccount.gender
					form.pet_type.data = stored_Paccount.type
					return render_template('pet_change.html', title='Modify your details', username=username, form=form, language=language[render_languages()])
			return render_template('pet_change.html', title='pet', user=user, username=username, form=form, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/pet_account', methods=['GET','POST'])
def pet_account():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
			prev_posts = Pet.query.filter(Pet.customer_id == customer_in_db.id ).all()
			return render_template('pet_account.html', title='pet', user=user, username=username, prev_posts=prev_posts, customer_in_db=customer_in_db, language=language[render_languages()] )
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/pet_add', methods=['GET','POST'])
def pet_add():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			if request.form.get("add")=='save':
				pet = Pet(name=request.form['name'], old=request.form['age'], gender=request.form['pet_gender'], type=request.form['pet_type'], owner=customer_db)
				db.session.add(pet)
				db.session.commit()
				return redirect(url_for('pet_account'))
			return render_template('pet_add.html', title='pet', user=user, username=username, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/pet_add_2', methods=['GET','POST'])
def pet_add_2():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			if request.form.get("add")=='save':
				pet = Pet(name=request.form['name'], old=request.form['age'], gender=request.form['pet_gender'], type=request.form['pet_type'], owner=customer_db)
				db.session.add(pet)
				db.session.commit()
				return redirect(url_for('reservation_s'))
			return render_template('pet_add.html', title='pet', user=user, username=username, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))



@app.route('/reservation_e', methods=['GET','POST'])
def reservation_e():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			pets_list=customer_db.pets
			if request.form.get("reservation_e")=='submit':
				pet_db=Pet.query.filter(Pet.name == request.form['pet_name'] ).first()
				emergency_appointment = Appointment(type='Emergency', pet_name=request.form['pet_name'], pet_type=pet_db.type, time=str(request.form['stime'])[11:16],date=str(request.form['stime'])[0:10], city=request.form['city'], details=request.form['details'], pet=pet_db, customer=customer_db)
				db.session.add(emergency_appointment)
				db.session.commit()
				return redirect(url_for('status_e'))
			return render_template('reservation_e.html', title='reservation', pets_list=pets_list, user=user, username=username, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/reservation_s', methods=['GET','POST'])
def reservation_s():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			pets_list=customer_db.pets
			if request.form.get("reservation_s")=='submit':
				pet_db=Pet.query.filter(Pet.name == request.form['pet_name'] ).first()
				standard_appointment = Appointment(type='Standard',pet_name=request.form['pet_name'],pet_type=pet_db.type, time=request.form['timeslot'], date=request.form['sdate'], city=request.form['city2'], details=request.form['details2'], pet=pet_db, customer=customer_db)
				db.session.add(standard_appointment)
				db.session.commit()
				return redirect(url_for('status_a'))
			return render_template('reservation_s.html', title='reservation', user=user, username=username, pets_list=pets_list, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_a', methods=['GET', 'POST'])
def status_a():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:
			return render_template('status_a.html', title='status', user=user, username=username, customer=customer_db, customer_in_db=customer_db, language=language[render_languages()] )
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_e', methods=['GET', 'POST'])
def status_e():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:	
			return render_template('status_e.html', title='status', user=user, username=username,  customer=customer_db,  customer_in_db=customer_db, language=language[render_languages()] )
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_sur', methods=['GET', 'POST'])
def status_sur():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		customer_db=Customer.query.filter(Customer.username==session.get("USERNAME")).first()
		if customer_db:	
			return render_template('status_sur.html', title='status', user=user, username=username, customer=customer_db, customer_in_db=customer_db, language=language[render_languages()] )
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/employee_register', methods=['GET', 'POST'])
def employee_register():
	session['current_path'] = request.path
	form = ERForm()
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		if employee_in_db:
			user = {'city': employee_in_db.key}
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
			return render_template('employee_register.html',user=user,title='Register a new employee', form=form, language=language[render_languages()])		
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/employee_c', methods=['GET', 'POST'])
def employee_c():
	session['current_path'] = request.path
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		if employee_in_db:
			user = {'city': employee_in_db.key}		
			prev_posts = db.session.query(Customer,Appointment,Pet).filter(Appointment.pet_id == Pet.id ).all()
			return render_template('employee_c.html', user=user,title='calendar', prev_posts=prev_posts, employee_in_db=employee_in_db, language=language[render_languages()] )
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/employee_t', methods=['GET', 'POST'])
def employee_t():
	session['current_path'] = request.path
	form=ManageForm()
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		if employee_in_db:
			if form.validate_on_submit():
				return redirect(url_for('employee_t'))
			else:
				user = {'city': employee_in_db.key}
				prev_posts = db.session.query(Customer, Appointment,Pet).filter(Appointment.customer_id == Customer.id).filter(Appointment.pet_id == Pet.id).filter(Appointment.city==employee_in_db.key).order_by(Appointment.type).all()
				return render_template('employee_t.html', user=user,form=form,d=form.date.data,title='table', prev_posts=prev_posts, employee_in_db=employee_in_db, language=language[render_languages()] )
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/employee_f', methods=['GET', 'POST'])
def employee_f():
	page = request.args.get('page', 1, type = int)
	session['current_path'] = request.path
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		if employee_in_db:
			user = {'city': employee_in_db.key}
			# app_in_db=Appointment.query.filter(Appointment.city==employee_in_db.key).first()
			prev_posts = db.session.query(Customer, Appointment,Pet).filter(Appointment.customer_id == Customer.id).filter(Appointment.pet_id == Pet.id).filter(Appointment.city==employee_in_db.key).order_by(Appointment.id.desc()).paginate(page, 6)
			return render_template('employee_f.html',user=user, title='table', prev_posts=prev_posts, language=language[render_languages()],pagination=prev_posts )
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/customer_chatting', methods=['GET', 'POST'])
def customer_chatting():
	session['current_path'] = request.path
	form = PostForm()
	username = session.get("USERNAME")
	if not session.get("USERNAME") is None:
		user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
		if user_in_db:
			if form.validate_on_submit():
				body = form.postbody.data
				post = Post(body=body, author = user_in_db, name=session.get("USERNAME"))
				db.session.add(post)
				db.session.commit()
				return redirect(url_for('customer_chatting'))
			else:
				prev_posts = Post.query.filter(Post.user_id == user_in_db.id).all()
				# print("Checking for user: {} with id: {}".format(user_in_db.username, user_in_db.id))
				return render_template('customer_chatting.html', title='Message', username=username, user_in_db=user_in_db, prev_posts=prev_posts, form=form, language=language[render_languages()])
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/employee_chatting', methods=['GET', 'POST'])
def employee_chatting():
	page = request.args.get('page', 1, type = int)
	session['current_path'] = request.path
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		if employee_in_db:
			user = {'city': employee_in_db.key}
			customers = Customer.query.filter().order_by(Customer.id).paginate(page, 1)
			return render_template('employee_chatting.html',user=user, title='Message', customers=customers,language=language[render_languages()],pagination=customers)
		else:
			flash("User not permitted")
			return redirect(url_for('login'))
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.pop("USERNAME", None)
	return redirect(url_for('index'))

#json code:
@app.route('/arrange',methods=['GET','POST'])
def arrange():
	list1=request.form.get('s')
	list1=list1.split(',')
	stored_app = Appointment.query.filter(Appointment.id == list1[0]).first()
	if stored_app:
		stored_app.date=list1[1]
		stored_app.time=list1[2]
		stored_app.type=list1[3]
		stored_app.status=list1[4]
		db.session.commit()
	s=list1[1]+','+list1[2]+','+list1[3]+','+list1[4]
	return jsonify(s)

@app.route('/delete',methods=['GET','POST'])
def delete():
	s=request.form.get('s')
	stored_app = Appointment.query.filter(Appointment.id == s).first()
	db.session.delete(stored_app)
	db.session.commit()
	return jsonify(s)

@app.route('/deletePet',methods=['GET','POST'])
def deletePet():
	s=request.form.get('s')
	stored_pet = Pet.query.filter(Pet.id == s).first()
	# stored_app = Appointment.query.filter(Appointment.pet_id == s).all()
	db.session.delete(stored_pet)
	# for a in stored_app:
	# 	db.session.delete(a)
	db.session.commit()
	return jsonify(s)

@app.route('/events')
def events():
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		app=db.session.query(Customer, Appointment,Pet).filter(Appointment.customer_id == Customer.id).filter(Appointment.pet_id == Pet.id).filter(Appointment.city==employee_in_db.key).all()
		ids=[]
		dates=[]
		time=[]
		status=[]
		types=[]
		for value in app:
			ids.append(value.Appointment.id)
			dates.append(value.Appointment.date)
			time.append(value.Appointment.time)
			status.append(value.Appointment.status)
			types.append(value.Appointment.type)
		l2=[]
		i=0
		while i<len(ids):
			dic={}
			if status[i]!='Submitted' and status[i]!='Fail':
				dic['title']='---ID: '+str(ids[i])
				dic['start']=dates[i]+'T'+time[i]+':00'
				if types[i]=='Standard':
					dic['color']='green'
				elif types[i]=='Emergency':
					dic['color']='pink'
				else:
					dic['color']='yellow'
			l2.append(dic)
			i=i+1
	return jsonify(l2)

@app.route('/message',methods=['GET','POST'])
def message():
	list1=request.form.get('s')
	list1=list1.split(',')
	customer = Customer.query.filter(Customer.username == list1[1]).first()
	post = Post(body=list1[0], author = customer, name=session.get("USERNAME"))
	db.session.add(post)
	db.session.commit()
	s=list1[1]
	return jsonify(s)
#end json code


@app.route('/detail')
def detail():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	return render_template('detail.html', title='detail', user=user, username=username, language=language[render_languages()] )


@app.route('/detail_a')
def detail_a():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	return render_template('detail_a.html', title='detail', user=user, username=username, language=language[render_languages()] )


@app.route('/detail_b')
def detail_b():
	session['current_path'] = request.path
	user = {'username': 'User'}
	username = session.get("USERNAME")
	return render_template('detail_b.html', title='detail', user=user, username=username, language=language[render_languages()] )


@app.route('/change_language')
def change_language():
    if session['lang'] == 'en':
        session['lang'] = 'cn'
        return redirect(session['current_path'])
    else:
        session['lang'] = 'en'
        return redirect(session['current_path'])

def render_languages():
    if not 'lang' in session:
        session['lang'] = 'en'
    return session['lang']


# @app.route('/base')
# def base():
# 	session['current_path'] = request.path
# 	# print(current_path)
# 	return render_template("base.html", language=language[render_languages()])

