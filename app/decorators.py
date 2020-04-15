from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission, State, Game

def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user.can(permission):
				print('failed permission required')
				abort(403)
			return f(*args,**kwargs)
		return decorated_function
	return decorator

def admin_required(f):
	return permission_required(Permission.ADMIN)(f)

def state_required(state):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			game = Game.query.filter_by(id=current_user.game_id).first()
			if game is not None:
				if not game.stateMatch(state):
					print('failed state required')
					abort(403)
			return f(*args,**kwargs)
		return decorated_function
	return decorator

def ingame_required(f):
	return state_required(State.INGAME)(f)

def countdown_required(f):
	return state_required(State.COUNTDOWN)(f)
