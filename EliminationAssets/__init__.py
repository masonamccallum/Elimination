import os
from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'  # We need to fix this. but it's okay for development

db_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(db_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'auth.login'

from EliminationAssets.main.views import main

app.register_blueprint(main)

# bootstrap = Bootstrap()
# db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

# def create_app(config_name):
# 	app = Flask(__name__)
# 	login_manager.init_app(app)
# 	app.config.from_object(config[config_name])
# 	config[config_name].init_app(app)
# 	bootstrap.init_app(app)
# 	db.init_app(app)
# 	#db.create_all()

# 	from .main import main as main_blueprint
# 	app.register_blueprint(main_blueprint)
	
# 	from .auth import auth as auth_blueprint
# 	app.register_blueprint(auth_blueprint, url_prefix='/auth')

# 	return app

