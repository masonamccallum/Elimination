from flask import Blueprint
from ..models import Permission

main = Blueprint('main',__name__)

from . import views


@main.app_context_processor
def injext_permissions():
	return dict(Permission=Permission)
