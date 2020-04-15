from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, StringField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired


class Rule(Form):
    ruleTitle = StringField('Title:')
    ruleToAdd = TextAreaField('Rule:')
    submit = SubmitField('Add Rule')


class AddRules(FlaskForm):
    rules = FieldList(
        FormField(Rule),
        min_entries=1,
        max_entries=20
    )


class EditRule(FlaskForm):
    editTitle = StringField('Edit Title:')
    editRule = TextAreaField('Edit Rule:')
    submit = SubmitField('Submit Edit')


class StartPoll(FlaskForm):
    ruleTitle = StringField('Title:')
    changeRule = TextAreaField('Rule:')
    submit = SubmitField('Change Rule')
    acceptDefault = SubmitField('Accept Defaults')