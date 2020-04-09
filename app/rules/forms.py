from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired


class AddRule(FlaskForm):
    ruleTitle = StringField('Title:');
    ruleToAdd = TextAreaField('Rule:')
    submit = SubmitField('Add Rule')


class EditRule(FlaskForm):
    editTitle = StringField('Edit Title:')
    editRule = TextAreaField('Edit Rule:')
    submit = SubmitField('Submit Edit')
