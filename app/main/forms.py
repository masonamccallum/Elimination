from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class newGameForm(FlaskForm):
	name= StringField('name',[validators.DataRequired()],render_kw = {"placeholder": "Title"})
	ruleTitle = StringField('Title: ')
	ruleBody = TextAreaField('Rule: ')
	countdownLength = IntegerField('Days till start', [validators.DataRequired()])
	submit = SubmitField('Create Game')

class joinGameForm(FlaskForm):
	code = StringField('Code',[validators.DataRequired()])
	submit = SubmitField('Join Game')
	
	def validate_gameid(self,field):
		if Game.query.filter_by(game_id=field.data).first():
			raise ValidationError('This is not a game id')
