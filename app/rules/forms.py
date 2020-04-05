from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired


class AddRule(FlaskForm):
    ruleTitle = StringField('Title:');
    ruleToAdd = TextAreaField('Rule:')
    submit = SubmitField('Add Rule')


class EditRule(FlaskForm):
    selectedRule = SelectField('Select Rule:')
    editRule = TextAreaField('Edit Here:')
    submit = SubmitField('Submit Edit')
