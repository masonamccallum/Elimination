from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired


class AddRule(FlaskForm):
    ruleToAdd = TextAreaField()
    submit = SubmitField('Add Rule')


class EditRule(FlaskForm):
    selectedRule = SelectField()
    submit = SubmitField('Submit Edit')
