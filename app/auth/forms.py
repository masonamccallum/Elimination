from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User
from wtforms import ValidationError


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(), Length(1,64), Email()],render_kw = {"placeholder": "example@gmail.com", "class":"form-control"})
	password = PasswordField('Password',validators=[DataRequired()],render_kw = {"placeholder": "password", "class":"form-control"})
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(), Length(1,64),Email()],render_kw = {"placeholder": "example@gmail.com", "class":"form-control"})
	username = StringField('Username', validators=[DataRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username not valid')],render_kw = {"placeholder": "Eliminator", "class":"form-control" })
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',message='Passwords must match.')],render_kw = {"placeholder": "Secrete ID", "class":"form-control" })
	password2 = PasswordField('Confirm Password', validators=[DataRequired()],render_kw = {"placeholder": "Confirm Password", "class":"form-control" })
	submit = SubmitField('Register')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already registered')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('User name is already used')
