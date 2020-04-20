from flask import render_template, session, redirect, url_for, flash
from random import shuffle
from . import main
from .forms import newGameForm, joinGameForm
from ..rules.forms import AddRules
from .. import db
from ..models import Game, User, Role, State
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..decorators import countdown_required, ingame_required
from datetime import datetime, timedelta
from flask import abort

@main.route('/')
def index():
	if current_user.is_authenticated:
		return redirect('/start')

	return render_template('login.html')

@main.route('/start')
def start():

	if current_user.is_anonymous:
		return redirect('/')
	else:
		user = User.query.filter_by(username=session['username']).first()
		game = user.game_id
	return render_template('index.html', game=game)


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

def assignTarget(game,player,target):
	user = game.users.filter_by(id=player).first()
	user.target_id = target
	db.session.commit()
	return

def map(arr,i):
	idx = arr[0].index(i)
	return arr[1][idx]

def reduce(arr):
	start = arr[1][0]
	i = map(arr,start)
	factor = [i]
	while(i is not start):
		i = map(arr,i)
		factor.append(i)
	return factor

def randomizeTargets(game_id):
	game = Game.query.filter_by(id=game_id).first()
	if game:
		userIDs = []
		users = game.users.all()
		for u in users:
			if u.role_id != 2:
				userIDs.append(u.id)
		temp = [userIDs,userIDs.copy()]
		shuffle(temp[1])
		while len(reduce(temp)) is not len(temp[0]):
			shuffle(temp[1])
		for player, targ in zip(temp[0],temp[1]):
			assignTarget(game,player,targ)	
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
			game = Game(name=form.name.data,ruleTitle=form.ruleTitle.data, ruleBody=form.ruleBody.data, countdownLength=cl)
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
		
@main.route('/leaveGame')
@login_required
def leaveGame():
	user =User.query.filter_by(username=session['username']).first()
	user.game_id = None
	db.session.commit()

	return redirect('/start')
