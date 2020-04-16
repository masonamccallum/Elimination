from flask import render_template, session, redirect, url_for, flash
from random import shuffle
from . import main
from .forms import newGameForm, joinGameForm
from .. import db
from ..models import Game, User, Role, State
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..decorators import countdown_required, ingame_required
from datetime import datetime, timedelta
from flask import abort

@main.route('/')
def index():
	return render_template('login.html')

@main.route('/start')
@login_required
def start():
	return render_template('index.html')

@main.route('/admin')
@login_required
@admin_required
def forAdmin():
	return '<h1>For ADMIN!!</h1>'

@main.route('/viewGameDetails/<game_id>',methods=['GET'])
@login_required
def viewGameInfo(game_id):
	game = Game.query.filter_by(id=game_id).first()
	if game:
		print(game)
		print(game.users.all())
	else:
		print('no game with that id')
	return '<h1>viewing Game Information</h1>'

def badShuffle(assign):
	for a in assign:
		if a[1].id == a[0] and len(assign) > 2:
			return True
		else:
			return False

def randomizeTargets(game_id):
	game = Game.query.filter_by(id=game_id).first()
	if game:
		users = game.users.all()
		numPlayers = len(users)
		targetList = list(range(1,numPlayers+1))
		for u in users:
			if u.is_administrator():
				targetList.remove(u.id)
				users.remove(u)
		
		assignments = list(zip(targetList,users))
		while badShuffle(assignments):
			shuffle(targetList)
			assignments = list(zip(targetList,users))

		print(assignments)
		for a in assignments:
			print(a[1])
			print(a[0])
			a[1].target_id = a[0]
		db.session.commit()
	else:
		print('error in Random Target assignment')

@main.route('/joinGame', methods=['GET','POST'])
@login_required
def joinGame():
	form = joinGameForm()
	if form.validate_on_submit():
		code = form.code.data
		game = Game.query.filter_by(id=code).first()
		if current_user.game_id is None:
			if game.stateMatch(State.COUNTDOWN):
				addToGame(code)
			else:
				flash('You are to late. That game has started')
				return redirect(url_for('main.start'))
		else:
			flash('You are already in a game')
		return redirect(url_for('main.countdown'))
	return render_template('joinGame.html',form=form)

def addToGame(code):
	user = User.query.filter_by(username=current_user.username).first()
	game = Game.query.filter_by(id=code)
	if user and game:
		if user.game_id is None:
			user.game_id = code
			db.session.commit()
			randomizeTargets(user.game_id)

@main.route('/createGame', methods=['GET','POST'])
@login_required
def createGame():
	form = newGameForm()
	if form.validate_on_submit():
		if current_user.game_id is None:
			cl = datetime.now()+timedelta(days=form.countdownLength.data)
			game = Game(name=form.name.data,rules=form.rules.data, countdownLength=cl)
			game.gameState = State.COUNTDOWN
			db.session.add(game)
			db.session.commit()
			g = Game.query.filter_by(name=form.name.data).first()
			if game:
				current_user.game_id = g.id
				current_user.role = Role.query.filter_by(name='Administrator').first()
				db.session.commit()
			else:	
				flash('create Game error')
			return redirect(url_for('main.countdown'))
		else:
			flash('You are already in a game')
	return render_template('createGame.html', form=form)

@main.route('/countdown',methods=['GET','POST'])
@login_required
@countdown_required
def countdown():
	return render_template('countdown.html')
	
@main.route('/gameStart',methods=['GET','POST'])
@login_required
@countdown_required
def gameStart():
	game = Game.query.filter_by(id=current_user.game_id).first()
	if game is not None:
		game.gameState = State.INGAME
		db.session.add(game)
		db.session.commit()
		game = Game.query.filter_by(id=current_user.game_id).first()
		print(game.gameState)
		print(Game.query.filter_by(gameState="ingame").first())
		return '<h1>game has started </h1>'
	else:
		return '<h1>game has failed to start</h1>'
		
