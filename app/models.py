from app import db

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first = db.Column(db.String())

class Card(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.String())
	image = db.Column(db.String())

	@property
	def serialize(self):
		return {
			'value': self.value,
			'image': self.image
		}

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	team = db.Column(db.String())
	image = db.Column(db.String())	 

	@property
	def serialize(self):
		return {
			'team': self.team,
			'image': self.image
		}

class Tile(db.Model):
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
	card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)
	team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
	position = db.Column(db.Integer)

	db.relationship('Game', uselist=False, backref='tiles', lazy='dynamic')
	db.relationship('Card', uselist=False, backref='tiles', lazy='dynamic')
	db.relationship('Role', uselist=False, backref='tiles', lazy='dynamic')

	def __init__(self, game, card, team, position):
		self.game_id = game.id
		self.card_id = card.id
		self.team_id = team.id
		self.position = position
