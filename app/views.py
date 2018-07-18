from PIL import Image, ImageFont, ImageDraw
from models import Card, Game, Team, Tile, db
from flask import jsonify, request
from app import app
import json
import os
import random

@app.route('/start')
def start():
	red = db.session.query(Team).filter_by(team='red').first()
	blue = db.session.query(Team).filter_by(team='blue').first()
	death = db.session.query(Team).filter_by(team='death').first()
	neutral = db.session.query(Team).filter_by(team='neutral').first()

	potential_first = [red, blue]
	first = potential_first[random.getrandbits(1)]

	game = Game(first=first.team)
	db.session.add(game)
	db.session.commit()
	db.session.refresh(game)

	tiles = (([red] * 8) + ([blue] * 8) + ([neutral] * 7) + [death] + [first])
	random.shuffle(tiles)
	deck = Card.query.all()
	random.shuffle(deck)
	cards = deck[:25]

	board = []
	results = {
		'game': game.id,
		'first': game.first,
		'cards': []
	}
	for idx, card in enumerate(cards):
		team = tiles.pop()
		cur_card = Tile(game, card, team, idx)
		db.session.add(cur_card)
		board.append(cur_card)
		results['cards'].append({
			'card': card.serialize,
			'team': team.serialize
		})

	db.session.commit()
	return jsonify(results)

@app.route('/reveal', methods=['GET'])
def reveal():
	position = request.args.get('position', None)
	game_id = request.args.get('game_id', None)
	tile = db.session.query(Tile).filter_by(game_id=game_id, position=position).first()
	tile.revealed = True
	db.session.commit()
	team = db.session.query(Team).filter_by(id=tile.team_id).first().team
	return team

@app.route('/end', methods=['PUT'])
def end():
	game_id = request.args.get('game_id', None)
	db.session.query(Tile).filter_by(game_id=game_id).delete()
	db.session.query(Game).filter_by(id=game_id).delete()
	db.session.commit()
	return jsonify()

@app.route('/list', methods=['GET'])
def list():
	game_id = request.args.get('game_id', None)
	results = {
		'cards': []
	}
	tiles = db.session.query(Tile).filter_by(game_id=game_id).all()
	for tile in tiles:
		card = db.session.query(Card).filter_by(id=tile.card_id).first()
		results['cards'].append({
			'position':tile.position,
			'card': card.serialize,
		})
	return jsonify(results)
