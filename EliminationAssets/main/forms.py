from flask_wtf import FlaskForm
from wtforms import *

class newGameForm(FlaskForm):
	rules = TextAreaField('Rules Here')#TODO make text file
	submit = SubmitField('Create Game')
