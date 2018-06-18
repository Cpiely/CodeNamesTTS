from models import Card, db
from flask import jsonify
from app import app
import json


@app.route('/')
def hello():
	return "Hello World!"

@app.route('/load')
def load_data():
	Card.query.delete()
	db.session.commit()
	with app.open_resource('static/cards.json') as f:
		data = json.load(f)
	for card in data:
		db.session.add(Card(value=card))
	db.session.commit()
	return jsonify(data)
