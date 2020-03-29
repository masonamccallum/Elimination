from EliminationAssets import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Game(db.Model):
	__tablename__='games'
	id = db.Column(db.Integer, primary_key=True)
	rules = db.Column(db.Text,nullable=False)
	users = db.relationship('User',backref='game')
	gameState = db.Column(db.String, nullable=False, default="preGame")
	#timer
	#proof
	#admin = db.relationship('User',backraf='game')
	def __repr__(self):
		return '<Game %r>' % self.id

class User(UserMixin,db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	game_id = db.Column(db.Integer, db.ForeignKey('games.id'))	

	@property
	def password(self):
		raise AttributeError('password is not readable')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % self.username

from . import login_manager
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
