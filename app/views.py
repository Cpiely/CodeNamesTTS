from PIL import Image, ImageFont, ImageDraw
from models import Card, Game, Team, Tile, db
from flask import jsonify
from app import app
import json
import os
import random

@app.route('/reset')
def reset():
	game = Game(first='blue')
	db.session.add(game)
	db.session.commit()
	db.session.refresh(game)

	red = db.session.query(Team).filter_by(team='red').first()
	blue = db.session.query(Team).filter_by(team='blue').first()
	death = db.session.query(Team).filter_by(team='death').first()
	neutral = db.session.query(Team).filter_by(team='neutral').first()

	tiles = (([red] * 8) + ([blue] * 9) + ([neutral] * 7) + [death])
	random.shuffle(tiles)
	deck = Card.query.all()
	random.shuffle(deck)
	cards = deck[:25]

	board = []
	results = []
	for idx, card in enumerate(cards):
		team = tiles.pop()
		cur_card = Tile(game, card, team, idx)
		db.session.add(cur_card)
		board.append(cur_card)
		results.append({
			'game': game.id,
			'card': card.serialize,
			'team': team.serialize
		})

	db.session.commit()

	return jsonify(results)
			


