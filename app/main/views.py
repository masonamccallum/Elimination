from flask import render_template, session, redirect, url_for
from . import main
from .forms import newGameForm
from .. import db
from ..models import Game


@main.route('/')
def index():
	return '<h1>INDEX</h1>'

@main.route('/viewExistingGames')
def viewGames():
	print(Game.query.all())
	return '<h1>viewGames</h1>'

@main.route('/viewGameDetails/<game_id>',methods=['GET'])
def viewGameInfo(game_id):
	game = Game.query.filter_by(id=game_id).all()
	if game:
		print(game)
		
	else:
		print('no game with that id')
	return '<h1>viewing Game Information</h1>'

@main.route('/createGame', methods=['GET','POST'])
def createGame():
	form = newGameForm()
	db.create_all()
	if form.validate_on_submit():
		game = Game(rules=form.rules.data)
		db.session.add(game)
		db.session.commit()
		return redirect('/viewExistingGames')
	return render_template('createGame.html', form=form)
