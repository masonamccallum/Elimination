from flask_wtf import FlaskForm
from wtforms import *

class newGameForm(FlaskForm):
	name= StringField('Group name: ',[validators.DataRequired()])
	ruleTitle = StringField('Title: ')
	ruleBody = TextAreaField('Rule: ')
	countdownLength = IntegerField('Days till start: ', [validators.DataRequired()])
	submit = SubmitField('Create Game!')

class joinGameForm(FlaskForm):
	code = StringField('Code',[validators.DataRequired()])
	submit = SubmitField('Join Game')
	
	def validate_gameid(self,field):
		if Game.query.filter_by(game_id=field.data).first():
			raise ValidationError('This is not a game id')
