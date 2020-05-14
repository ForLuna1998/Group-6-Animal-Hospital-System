
from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField, DateField, RadioField, FileField, TextAreaField
from wtforms.validators import DataRequired,ValidationError
from flask_wtf.file import FileRequired, FileAllowed

from blogapp.models import Pet, Customer


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Username...","required":'required'})
	password = PasswordField('Password', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Password...","required":'required'})
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In',render_kw={"class":"btn"})
	
#render_kw: https://www.cnblogs.com/FRESHMANS/p/8529992.html
class CRForm(FlaskForm):
	username = StringField('', validators=[DataRequired()],description="Username",render_kw={"class":"form-control","placeholder":"Username...","required":'required'})
	email = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Email...","required":'required'})
	password = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Password...","required":'required'})
	password2 = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Repeat Password...","required":'required'})
	accept_rules = BooleanField('I accept the ', validators=[DataRequired()])
	submit = SubmitField('Sign up',render_kw={"class": "btn btn-primary btn-block btn-flat"})

class ERForm(FlaskForm):
	username = StringField('', validators=[DataRequired()],description="Username",render_kw={"class":"form-control","placeholder":"Username...","required":'required'})
	key = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Place Key...","required":'required'})
	password = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Password...","required":'required'})
	password2 = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Repeat Password...","required":'required'})
	accept_rules = BooleanField('I accept the ', validators=[DataRequired()])
	submit = SubmitField('Register',render_kw={"class": "btn btn-primary btn-block btn-flat"})


class CustomerAccountForm(FlaskForm):
	firstname = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Firstname...","required":'required'})
	lastname = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Lastname...","required":'required'})
	email = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Email...","required":'required'})
	telephone = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Telephone...","required":'required'})
	save = SubmitField('Save change', render_kw={"class": "btn btn-primary "})

class CustomerPasswordForm(FlaskForm):
	password = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Old Password...","required":'required'})
	password2 = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"New Password...","required":'required'})
	password3 = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","placeholder":"Retype Password...","required":'required'})
	pas = SubmitField('Set new password', render_kw={"class": "btn btn-primary "})


class PetAccountForm(FlaskForm):
	# pet_id = SelectField('', validators=[DataRequired()], choices=[('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D')],
	# 					 render_kw={"class": "form-control", "placeholder": "Select your pet here.",
	# 								"required": 'required'})
	pet_id = SelectField('', coerce=int, validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Select your pet here.", "required": 'required'})

	pet_name = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control", "placeholder": "Name", "required": 'required'})
	pet_age = StringField('', validators=[DataRequired()],
						  render_kw={"class": "form-control", "placeholder": "Old", "required": 'required'})
	pet_gender = StringField('', validators=[DataRequired()],
							 render_kw={"class": "form-control", "placeholder": "Gender", "required": 'required'})
	pet_type = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control", "placeholder": "Type", "required": 'required'})
	save = SubmitField('Save change', render_kw={"class": "btn btn-primary "})

	def __init__(self, *args, **kwargs):
		super(PetAccountForm, self).__init__(*args, **kwargs)
		if not session.get("USERNAME") is None:
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			self.pet_id.choices=[(pet_id.id,pet_id.name) for pet_id in Pet.query.filter(Pet.customer_id == customer_in_db.id).all()]

class PetDeleteForm(FlaskForm):
	# pet_id = SelectField('', validators=[DataRequired()], choices=[('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D')],
	# 					 render_kw={"class": "form-control", "placeholder": "Select your pet here.",
	# 								"required": 'required'})
	pet_id = SelectField('', coerce=int, validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Select your pet here.", "required": 'required'})

	delete = SubmitField('Delete', render_kw={"class": "btn btn-primary"})

	def __init__(self, *args, **kwargs):
		super(PetDeleteForm, self).__init__(*args, **kwargs)
		if not session.get("USERNAME") is None:
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			self.pet_id.choices=[(pet_id.id,pet_id.name) for pet_id in Pet.query.filter(Pet.customer_id == customer_in_db.id).all()]


class REForm(FlaskForm):
	# pet_id = SelectField('', validators=[DataRequired()], choices=[('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D')],
	# 					 render_kw={"class": "form-control", "placeholder": "Select your pet here.",
	# 								"required": 'required'})
	pet_id = SelectField('', coerce=int, validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Select your pet here.", "required": 'required'})
	time = StringField('', validators=[DataRequired()], 
						 render_kw={"class": "form-control", "required": 'required'})
	city = SelectField('', validators=[DataRequired()], choices=[('Beijing', 'Beijing'), ('Shanghai', 'Shanghai'), ('Chengdu', 'Chengdu')]
						 ,render_kw={"class": "form-control", "required": 'required'})
	detail = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control", "placeholder": "Details...", "required": 'required'})
	submit = SubmitField('Submit', render_kw={"class": "btn btn-primary "})

	def __init__(self, *args, **kwargs):
		super(REForm, self).__init__(*args, **kwargs)
		if not session.get("USERNAME") is None:
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			self.pet_id.choices=[(pet_id.id,pet_id.name) for pet_id in Pet.query.filter(Pet.customer_id == customer_in_db.id).all()]

class RSForm(FlaskForm):
	# pet_id = SelectField('', validators=[DataRequired()], choices=[('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D')],
	# 					 render_kw={"class": "form-control", "placeholder": "Select your pet here.",
	# 								"required": 'required'})
	pet_id = SelectField('', coerce=int, validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Select your pet here.", "required": 'required'})

	date = StringField('', validators=[DataRequired()],
						   render_kw={ "class": "form-control","placeholder": "Select date...", "required": 'required'})
	time = SelectField('', validators=[DataRequired()], choices=[('morning', 'morning'), ('afternoon', 'afternoon'), ('evening', 'evening')],
						 render_kw={"class": "form-control", "placeholder": "Select your pet here.",
									"required": 'required'})
	city = SelectField('', validators=[DataRequired()], choices=[('Beijing', 'Beijing'), ('Shanghai', 'Shanghai'), ('Chengdu', 'Chengdu')]
						 ,render_kw={"class": "form-control", "required": 'required'})
	detail = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control", "placeholder": "Details...", "required": 'required'})
	submit = SubmitField('Submit', render_kw={"class": "btn btn-primary "})

	def __init__(self, *args, **kwargs):
		super(RSForm, self).__init__(*args, **kwargs)
		if not session.get("USERNAME") is None:
			customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
			self.pet_id.choices=[(pet_id.id,pet_id.name) for pet_id in Pet.query.filter(Pet.customer_id == customer_in_db.id).all()]

class PetChangeForm(FlaskForm):
	pet_name = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control", "placeholder": "Name", "required": 'required'})
	pet_age = StringField('', validators=[DataRequired()],
						  render_kw={"class": "form-control", "placeholder": "Old", "required": 'required'})
	pet_gender = SelectField('', validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female')],
						 render_kw={"class": "form-control", "placeholder": "Select your pet here.",
									"required": 'required'})
	pet_type = SelectField('', validators=[DataRequired()],choices=[('Dog', 'Dog'), ('Cat', 'Cat')],
						   render_kw={"class": "form-control", "placeholder": "Type", "required": 'required'})
	save = SubmitField('Save change', render_kw={"class": "btn btn-primary "})
		
class PetAddForm(FlaskForm):
	pet_name = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control", "placeholder": "Name", "required": 'required'})
	pet_age = StringField('', validators=[DataRequired()],
						  render_kw={"class": "form-control", "placeholder": "Old", "required": 'required'})
	pet_gender = SelectField('', validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female')],
							 render_kw={"class": "form-control", "placeholder": "Gender", "required": 'required'})
	pet_type = SelectField('', validators=[DataRequired()],choices=[('Dog', 'Dog'), ('Cat', 'Cat')],
						   render_kw={"class": "form-control", "placeholder": "Type", "required": 'required'})
	submit = SubmitField('Add new pet', render_kw={"class": "btn btn-primary "})

class PostForm(FlaskForm):
	postbody = StringField('Chatbox', validators=[DataRequired()])
	submit = SubmitField('Send')

class PostForm2(FlaskForm):
	postbody = StringField('Chatbox', validators=[DataRequired()])
	who=StringField('To user: ', validators=[DataRequired()])
	submit = SubmitField('Send')

class ManageForm(FlaskForm):
	date=StringField('',render_kw={"style": "font-size: large;", "placeholder": "YYYY-MM-DD", "required": 'required'})
	submit = SubmitField('Search',render_kw={"class": "btn btn-primary edit"})

