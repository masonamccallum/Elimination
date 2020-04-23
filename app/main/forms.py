from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, validators

class newGameForm(FlaskForm):
    """Form for new game"""
    name = StringField('name', [validators.DataRequired()], render_kw={"placeholder": "Title"})
    ruleTitle = StringField('Title: ')
    ruleBody = TextAreaField('Rule: ')
    countdownLength = IntegerField('Days till start', [validators.DataRequired()], \
                                    render_kw={"placeholder": "Days Until Game Start"})
    submit = SubmitField('Create Game')

class joinGameForm(FlaskForm):
    """Form for joining a game"""
    code = StringField('Code',[validators.DataRequired()])
    submit = SubmitField('Join Game')
    def validate_gameid(self, field):
        """Validate game id"""
        if Game.query.filter_by(game_id=field.data).first():
            raise ValidationError('This is not a game id')
