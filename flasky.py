import os
from app import create_app, db

from app.models import User, Game, Role, Permission, Rule, Poll


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Game=Game, Role=Role, Permission=Permission, Rule=Rule, Poll=Poll)
