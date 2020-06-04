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
	submit = SubmitField('Sign in',render_kw={"class":"btn btn-primary btn-block btn-flat"})
	
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
	submit = SubmitField('Register',render_kw={"class": "btn btn-primary btn-block btn-flat"})


class CustomerAccountForm(FlaskForm):
	firstname = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","required":'required'})
	lastname = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","required":'required'})
	email = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","required":'required'})
	telephone = StringField('', validators=[DataRequired()],render_kw={"class":"form-control","required":'required'})
	save = SubmitField('Save changes', render_kw={"class": "btn btn-primary "})

class CustomerPasswordForm(FlaskForm):
	password = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","required":'required'})
	password2 = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","required":'required'})
	password3 = PasswordField('', validators=[DataRequired()],render_kw={"class":"form-control","required":'required'})
	pas = SubmitField('Set new password', render_kw={"class": "btn btn-primary "})


class PetAccountForm(FlaskForm):
	pet_id = SelectField('', coerce=int, validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Select your pet here.", "required": 'required'})

	pet_name = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control", "required": 'required'})
	pet_age = StringField('', validators=[DataRequired()],
						  render_kw={"class": "form-control",  "required": 'required'})
	pet_gender = StringField('', validators=[DataRequired()],
							 render_kw={"class": "form-control",  "required": 'required'})
	pet_type = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control",  "required": 'required'})
	save = SubmitField('Save changes', render_kw={"class": "btn btn-primary "})


class PetChangeForm(FlaskForm):
	pet_name = StringField('', validators=[DataRequired()],
						   render_kw={"class": "form-control",  "required": 'required'})
	pet_age = StringField('', validators=[DataRequired()],
						  render_kw={"class": "form-control",  "required": 'required'})
	pet_gender = SelectField('', validators=[DataRequired()], choices=[('Male', 'Male'), ('Female', 'Female')],
						 render_kw={"class": "form-control", 
									"required": 'required'})
	pet_type = SelectField('', validators=[DataRequired()],choices=[('Dog', 'Dog'), ('Cat', 'Cat')],
						   render_kw={"class": "form-control",  "required": 'required'})
	save = SubmitField('Save changes', render_kw={"class": "btn btn-primary "})


class PostForm(FlaskForm):
	postbody = StringField('Chatbox', validators=[DataRequired()],render_kw={"class": "form-control", "required": 'required'})
	submit = SubmitField('Send', render_kw={"class": "btn btn-primary "})

class ManageForm(FlaskForm):
	date=StringField('',render_kw={"style": "font-size: large;", "placeholder": "YYYY-MM-DD", "required": 'required'})
	submit = SubmitField('Search',render_kw={"class": "btn btn-primary edit"})

