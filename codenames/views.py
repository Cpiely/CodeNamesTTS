
from models import Card
from flask import Blueprint, jsonify
from app import db, app
import json

codenames_app = Blueprint('codenames', __name__)

@codenames_app.route('/')
def hello():
    return "Hello World!"

@codenames_app.route('/load')
def load_data():
    Card.query.delete()
    db.session.commit()
    with app.open_resource('static/cards.json') as f:
    	data = json.load(f)
    for card in data:
    	db.session.add(Card(value=card))
    db.session.commit()
    return jsonify(data)
