import os
import argparse
import json
from imgurpython import ImgurClient
from PIL import Image, ImageFont, ImageDraw
from app import app, db, models


parser = argparse.ArgumentParser()

client_id = os.environ.get('CLIENT_ID', None)
client_secret = os.environ.get('CLIENT_SECRET', None)
access_token = os.environ.get('ACCESS_TOKEN', None)
refresh_token = os.environ.get('REFRESH_TOKEN', None)

client = ImgurClient(client_id, client_secret)

client.set_user_auth(access_token, refresh_token)

def upload_cards(album):
	images = client.get_album_images(album)
	with app.open_resource('static/data/cards.json') as f:
		data = sorted(json.load(f))
	for card, image in zip(data,images):
		db.session.add(models.Card(value=card, image=image.link))
	db.session.commit()

def upload_teams(album):
	teams = ['red', 'neutral', 'death', 'blue']
	images = client.get_album_images(album)
	for team, image in zip(teams, images):
		db.session.add(models.Team(team=team, image=image.link))
	db.session.commit()

def main():
	card_album_id = 'U2JcLRR'
	upload_cards(card_album_id)
	teams_album_id = 'GlBh9Lx'
	upload_teams(teams_album_id)

if __name__ == '__main__':
	main()
