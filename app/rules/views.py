from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import rules
# from ..models import Rule
from .forms import AddRule, EditRule


@rules.route('/createRule', methods=['GET','POST'])
# @login_required
def create():
    form = AddRule()
    if form.validate_on_submit():
        createdRule = Rule(title=form.ruleTitle.data,
                            body=form.ruleToAdd.data)
        db.session.add(createdRule)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('rules/add_rules.html', form=form)


@rules.route('/editRule/<int:rule_id>', methods=['GET','POST'])
# @login_required
def edit():
    form = EditRule()
    return render_template('rules/edit_rules.html', form=form)

