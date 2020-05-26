from flask import render_template, flash, redirect, url_for, session,request,jsonify,json
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp import app, db
from blogapp.forms import LoginForm, ERForm, CRForm, PetAccountForm, CustomerAccountForm, REForm, RSForm, PetAddForm, CustomerPasswordForm, PetDeleteForm, PetChangeForm,PostForm, PostForm2, ManageForm
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
	return render_template('index.html', title='Home', language=language[render_languages()])


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

@app.route("/customer_base")
def customer_base():
	session['current_path'] = request.path
	session['current_patth']=request.path
	return render_template('customer_base.html', language=language[render_languages()])

@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
	session['current_path'] = request.path
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
	return render_template('customer_register.html', title='Register a new user', form=form, language=language[render_languages()])


@app.route('/employee_register', methods=['GET', 'POST'])
def employee_register():
	session['current_path'] = request.path
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
	return render_template('employee_register.html', title='Register a new employee', form=form, language=language[render_languages()])


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
		return render_template('customer_index.html', title='Home', user=user, language=language[render_languages()])
	else:
		flash("User needs to either login or sign up")
		return redirect(url_for('index'))

@app.route('/customer_account', methods=['GET','POST'])
def customer_account():
	session['current_path'] = request.path
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
				return render_template('customer_account.html', title='Init your details', form=form, language=language[render_languages()])
			else:
				form.email.data = stored_account.email
				form.firstname.data = stored_account.firstname
				form.lastname.data = stored_account.lastname
				form.telephone.data = stored_account.phone
				return render_template('customer_account.html', title='Modify your details', form=form, language=language[render_languages()])
		return render_template('customer_account.html', title='pet', user=user, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/customer_password', methods=['GET', 'POST'])
def customer_password():
	session['current_path'] = request.path
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
		return render_template('customer_password.html', title='pet', user=user, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/pet_change', methods=['GET','POST'])
def pet_change():
	session['current_path'] = request.path
	user = {'username': 'User'}
	form = PetChangeForm()
	if not session.get("USERNAME") is None:
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
				return render_template('pet_change.html', title='Init your details', form=form, language=language[render_languages()])
			else:
				form.pet_name.data = stored_Paccount.name
				form.pet_age.data = stored_Paccount.old
				form.pet_gender.data = stored_Paccount.gender
				form.pet_type.data = stored_Paccount.type
				return render_template('pet_change.html', title='Modify your details', form=form, language=language[render_languages()])
		return render_template('pet_change.html', title='pet', user=user, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/pet_account', methods=['GET','POST'])
def pet_account():
	session['current_path'] = request.path
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = Pet.query.filter(Pet.customer_id == customer_in_db.id ).all()
		return render_template('pet_account.html', title='pet', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db, language=language[render_languages()] )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/pet_add', methods=['GET','POST'])
def pet_add():
	session['current_path'] = request.path
	user = {'username': 'User'}
	form = PetAddForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			pet = Pet(name=form.pet_name.data, old=form.pet_age.data, gender=form.pet_gender.data, type=form.pet_type.data, customer_id=customer_in_db.id)
			db.session.add(pet)
			db.session.commit()
			return redirect(url_for('pet_account'))
		return render_template('pet_add.html', title='reservation', user=user, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/pet_delete', methods=['GET', 'POST'])
def pet_delete():
	session['current_path'] = request.path
	user = {'username': 'User'}
	form = PetDeleteForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			pet_in_db = Pet.query.filter(Pet.id == form.pet_id.data).first()
			Appointment.query.filter(Appointment.pet_id == form.pet_id.data).delete(synchronize_session=False)
			db.session.delete(pet_in_db)
			db.session.commit()
			return redirect(url_for('pet_account'))
		return render_template('pet_delete.html', title='pet', user=user, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/reservation_e', methods=['GET','POST'])
def reservation_e():
	session['current_path'] = request.path
	user = {'username': 'User'}
	form = REForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			#存到数据库的日期和时间格式分别是yyyy-mm-dd 和 hh:mm
			emergency_appointment = Appointment(type='Emergency', time=str(form.time.data)[11:16],date=str(form.time.data)[0:10], 
				city=form.city.data, details=form.detail.data, pet_id=form.pet_id.data, customer=customer_in_db)
			db.session.add(emergency_appointment)
			db.session.commit()
			return redirect(url_for('status_e'))
		return render_template('reservation_e.html', title='reservation', user=user, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/reservation_s', methods=['GET','POST'])
def reservation_s():
	session['current_path'] = request.path
	user = {'username': 'User'}
	form = RSForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			standard_appointment = Appointment(type='Standard',date=form.date.data, time=form.time.data, city=form.city.data, 
				details=form.detail.data,  pet_id=form.pet_id.data, customer=customer_in_db)
			db.session.add(standard_appointment)
			db.session.commit()
			return redirect(url_for('status_a'))
		return render_template('reservation_s.html', title='reservation', user=user, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_a', methods=['GET', 'POST'])
def status_a():
	session['current_path'] = request.path
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		return render_template('status_a.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db, language=language[render_languages()] )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_e', methods=['GET', 'POST'])
def status_e():
	session['current_path'] = request.path
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		return render_template('status_e.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db, language=language[render_languages()] )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/status_sur', methods=['GET', 'POST'])
def status_sur():
	session['current_path'] = request.path
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		# prev_posts = Appointment.query.filter(Appointment.type=='Surgery' ).all()
		return render_template('status_sur.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db, language=language[render_languages()] )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/record_a', methods=['GET', 'POST'])
def record_a():
	session['current_path'] = request.path
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		return render_template('record_a.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db,  language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/record_e', methods=['GET', 'POST'])
def record_e():
	session['current_path'] = request.path
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		return render_template('record_e.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db,  language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/record_o', methods=['GET', 'POST'])
def record_o():
	session['current_path'] = request.path
	user = {'username': 'User'}
	if not session.get("USERNAME") is None:
		customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()		
		prev_posts = db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id ).all()
		# prev_posts = Appointment.query.filter(Appointment.status==4 ).all()
		return render_template('record_o.html', title='record', user=user, prev_posts=prev_posts, customer_in_db=customer_in_db, language=language[render_languages()] )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/employee_c', methods=['GET', 'POST'])
def employee_c():
	session['current_path'] = request.path
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		user = {'city': employee_in_db.key}		
		prev_posts = db.session.query(Customer, Appointment).filter(Customer.id == Appointment.customer_id ).all()
		return render_template('employee_c.html', user=user,title='calendar', prev_posts=prev_posts, employee_in_db=employee_in_db, language=language[render_languages()] )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/employee_t', methods=['GET', 'POST'])
def employee_t():
	session['current_path'] = request.path
	form=ManageForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			return redirect(url_for('employee_t'))
		else:
			employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
			user = {'city': employee_in_db.key}
			prev_posts = db.session.query(Customer, Appointment).filter(Customer.id == Appointment.customer_id ).order_by(Appointment.type).all()
			return render_template('employee_t.html', user=user,form=form,d=form.date.data,title='table', prev_posts=prev_posts, employee_in_db=employee_in_db, language=language[render_languages()] )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/employee_f', methods=['GET', 'POST'])
def employee_f():
	page = request.args.get('page', 1, type = int)
	session['current_path'] = request.path
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		user = {'city': employee_in_db.key}
		# app_in_db=Appointment.query.filter(Appointment.city==employee_in_db.key).first()
		prev_posts = db.session.query(Customer, Appointment).filter(Customer.id == Appointment.customer_id ).order_by(Appointment.id.desc()).paginate(page, 6)
		return render_template('employee_f.html',user=user, title='table', prev_posts=prev_posts, employee_in_db=employee_in_db, language=language[render_languages()],pagination=prev_posts )
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.route('/customer_chatting', methods=['GET', 'POST'])
def customer_chatting():
	session['current_path'] = request.path
	form = PostForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			body = form.postbody.data
			user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			post = Post(body=body, author = user_in_db, name=session.get("USERNAME"))
			db.session.add(post)
			db.session.commit()
			return redirect(url_for('customer_chatting'))
		else:
			user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			prev_posts = Post.query.filter(Post.user_id == user_in_db.id).all()
			# print("Checking for user: {} with id: {}".format(user_in_db.username, user_in_db.id))
			return render_template('customer_chatting.html', title='Message', prev_posts=prev_posts, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/employee_chatting', methods=['GET', 'POST'])
def employee_chatting():
	session['current_path'] = request.path
	form = PostForm2()
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		user = {'city': employee_in_db.key}
		if form.validate_on_submit():
			body = form.postbody.data
			who=form.who.data
			user_in_db = Customer.query.filter(Customer.username == who).first()
			if user_in_db:
				post = Post(body = body, author = user_in_db, name=session.get("USERNAME"))
				db.session.add(post)
				db.session.commit()
			return redirect(url_for('employee_chatting'))
		else:
			# user_in_db = Customer.query.first()
			prev_posts = Post.query.all()
			# print("Checking for user: {} with id: {}".format(user_in_db.username, user_in_db.id))
			return render_template('employee_chatting.html',user=user, title='Message', prev_posts=prev_posts, form=form, language=language[render_languages()])
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))

@app.route('/arrange',methods=['GET','POST'])
def arrange():
	list1=request.form.get('s')
	list1=list1.split(',')
	stored_app = Appointment.query.filter(Appointment.id == list1[0]).first()
	if stored_app:
		stored_app.date=list1[3]
		stored_app.time=list1[4]
		stored_app.type=list1[5]
		stored_app.status=list1[6]
		db.session.commit()
	s=list1[0]+','+list1[1]+','+list1[2]+','+list1[3]+','+list1[4]+','+list1[5]+','+list1[6]
	return jsonify(s)

@app.route('/logout')
def logout():
	session.pop("USERNAME", None)
	return redirect(url_for('login'))

@app.route('/detail')
def detail():
	session['current_path'] = request.path
	print(current_path)
	user = {'username': 'User'}
	return render_template('detail.html', title='detail', user=user, language=language[render_languages()] )

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

@app.route('/base')
def base():
	session['current_path'] = request.path
	# print(current_path)
	return render_template("base.html", language=language[render_languages()])

@app.route('/events')
def events():
	if not session.get("USERNAME") is None:
		employee_in_db = Employee.query.filter(Employee.username == session.get("USERNAME")).first()
		app=Appointment.query.filter(Appointment.city==employee_in_db.key).group_by(Appointment.id)
		ids=[]
		dates=[]
		time=[]
		status=[]
		types=[]
		for value in Appointment.query.filter(Appointment.city==employee_in_db.key).group_by(Appointment.id):
			ids.append(value.id)
			dates.append(value.date)
			time.append(value.time)
			status.append(value.status)
			types.append(value.type)
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
