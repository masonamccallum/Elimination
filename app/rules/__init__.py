from flask import Blueprint

rules = Blueprint('rules', __name__)

from . import views