from app import db

class Card(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.String())

	def __repr__(self):
		return '<value {}>'.format(self.value)