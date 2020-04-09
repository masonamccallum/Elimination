from flask_wtf import FlaskForm
from wtforms import *

class newGameForm(FlaskForm):
	rules = TextAreaField('Rules Here')#TODO make text file
	submit = SubmitField('Create Game')

class joinGameForm(FlaskForm):
	code = StringField('Code',[validators.DataRequired()])
	submit = SubmitField('Join Game')
	
	def validate_gameid(self,field):
		if Game.query.filter_by(game_id=field.data).first():
			raise ValidationError('This is not a game id')
