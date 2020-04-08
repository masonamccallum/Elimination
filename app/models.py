from . import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

class Permission:
	CREATEPOLL = 1
	VOTEPOLL = 2
	KICKPLAYER = 4
	ADMIN = 8

class Game(db.Model):
	__tablename__='games'
	id = db.Column(db.Integer, primary_key=True)
	rules = db.Column(db.Text,nullable=False)
	users = db.relationship('User',backref='game')
	gameState = db.Column(db.String, nullable=False, default="preGame")
	users = db.relationship('User',backref='game', lazy='dynamic')
	def verify_gameid(self,gameId):
		if Game.query.filter_by(game_id=gameId):
			return True
		else:
			return False

	def __repr__(self):
		return '<Game %r>' % self.id

class User(UserMixin,db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	game_id = db.Column(db.Integer, db.ForeignKey('games.id'))	
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	@property
	def password(self):
		raise AttributeError('password is not readable')
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	def __repr__(self):
		return f'<User {self.username} {self.role_id}>' 
	
	def can(self,perm):
		return self.role is not None and self.role.has_permission(perm)

	def is_administrator(self):
		return self.can(Permission.ADMIN)

	def __init__(self,**kwargs):
		super(User,self).__init__(**kwargs)
		if self.role is None:
			if self.email == 'm@gmail.com':
				self.role = Role.query.filter_by(name='Administrator').first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False
	
	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User',backref='role', lazy='dynamic')
	
	@staticmethod
	def insert_roles():
		roles = {
			'Player': [Permission.VOTEPOLL],
			'Administrator': [Permission.ADMIN, Permission.CREATEPOLL, Permission.KICKPLAYER]
		}
		
		default_role = 'Player'

		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.reset_permissions()
			for perm in roles[r]:
				role.add_permission(perm)
			role.default = (role.name==default_role)
			db.session.add(role)
		db.session.commit()

	
	def add_permission(self,perm):
		if not self.has_permission(perm):
			self.permissions += perm

	def remove_permission(self,perm):
		if self.has_permission(perm):
			self.permissions -= perm
	
	def reset_permissions(self):
		self.permissions = 0
	
	def has_permission(self,perm):
		return self.permissions & perm == perm
	
	def __repr__(self):
		return '<Role %r>' % self.name

	def __init__(self, **kargs):
		super(Role,self).__init__(**kargs)
		if self.permissions is None:
			self.permissions = 0

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
