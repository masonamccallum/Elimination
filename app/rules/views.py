from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import rules
from ..models import Rule
from .. import db
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
    return render_template('rules/add_rule.html', form=form)

@rules.route('/<int:rule_id>')
def rule(rule_id):
    rule = Rule.query.get_or_404(rule_id)
    return render_template('rules/rule.html', title=rule.title,
                            body=rule.body)


@rules.route('/editRule/<int:rule_id>', methods=['GET','POST'])
# @login_required
def edit(rule_id):
    rule = Rule.query.get_or_404(rule_id)
    form = EditRule()

    if form.validate_on_submit():
        rule.title = form.selecRule.select
        rule.body = form.editRule.data

        db.session.commit()
        return redirect(url_for('rules.rule', rule_id=rule_id))

    elif request.method == 'GET':
        form.selectRule.data = rule.title
        form.body.data = rule.body

    return render_template('rules/edit_rule.html', form=form)


@rules.route('/deleteRule/<int:rule_id>', methods=['GET','POST'])
# @login_required
def delete(rule_id):
    rule = Rule.query.get_or_404(rule_id)

    db.session.delete(rule)
    db.session.commit()
    return redirect(url_for('main.index'))
    