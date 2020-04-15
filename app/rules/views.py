from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import rules
from ..models import Rule, Poll
from .. import db
from .forms import AddRules, EditRule



    