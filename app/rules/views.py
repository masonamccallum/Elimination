from flask import render_template, redirect, request, url_for, flash
from .. import db
from flask_login import login_required
from .forms import AddRule, EditRule

@rules.route('/createRule', methods=['GET','POST'])
@login_required
def create():
    form = AddRule()
    return render_template('rules/add_rules.html', form=form)


@rules.route('/editRule', methods=['GET','POST'])
@login_required
def edit():
    form = EditRule()
    return render_template('rules/edit_rules.html', form=form)

