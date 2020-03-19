from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# render_kw: https://www.cnblogs.com/FRESHMANS/p/8529992.html
class SignupForm(FlaskForm):
    username = StringField('', validators=[DataRequired()], description="Username",
                           render_kw={"class": "form-control", "placeholder": "Username", "required": 'required'})
    email = StringField('', validators=[DataRequired()],
                        render_kw={"class": "form-control", "placeholder": "Email", "required": 'required'})
    password = PasswordField('', validators=[DataRequired()],
                             render_kw={"class": "form-control", "placeholder": "Password", "required": 'required'})
    password2 = PasswordField('', validators=[DataRequired()],
                              render_kw={"class": "form-control", "placeholder": "Repeat Password",
                                         "required": 'required'})
    accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
    submit = SubmitField('Sign up', render_kw={"class": "btn btn-primary btn-block btn-flat"})
