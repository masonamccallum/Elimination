from flask import Flask, render_template, session, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

bootstrap = Bootstrap(app)

class newGameForm(FlaskForm):
	ruleSet = TextAreaField('Rules Here')#TODO make text file
	submit = SubmitField('Create Game')

@app.shell_context_processor
def make_shell_context():
	return dict(db=db,User=User, Game=Game)

class Game(db.Model):
	__tablename__='games'
	id = db.Column(db.Integer, primary_key=True)
	#rules = db.Column(db.Text,nullable=False)
	users = db.relationship('User',backref='game')
	def __repr__(self):
		return '<Game %r>' % self.id

class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, index=True)
	game_id = db.Column(db.Integer, db.ForeignKey('games.id'))	

	def __repr__(self):
		return '<User %r>' % self.name


@app.route('/')
def index():
	return '<h1>INDEX</h1>'

@app.route('/viewExistingGames')
def viewGames():
	db.create_all()
	print(Game.query.all())
	return '<h1>viewGames</h1>'

@app.route('/createGame', methods=['GET','POST'])
def createGame():
	form = newGameForm()
	db.create_all()
	if form.validate_on_submit():
		game = Game()
		db.session.add(game)
		db.session.commit()
		return redirect('/viewExistingGames')
	return render_template('createGame.html', form=form)
	
if __name__ == '__main__':
	app.run(debug=True)
