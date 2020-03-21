from . import db

class Game(db.Model):
	__tablename__='games'
	id = db.Column(db.Integer, primary_key=True)
	rules = db.Column(db.Text,nullable=False)
	users = db.relationship('User',backref='game')
	#admin = db.relationship('User',backraf='game')
	def __repr__(self):
		return '<Game %r>' % self.id

class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, index=True)
	game_id = db.Column(db.Integer, db.ForeignKey('games.id'))	

	def __repr__(self):
		return '<User %r>' % self.name
