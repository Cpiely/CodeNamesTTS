import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

def create_app(config):

	app.config.from_object(config)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	
	db.init_app(app)

	from codenames.views import codenames_app
	
	app.register_blueprint(codenames_app)

	return app
