from src import app
import sys, json, requests
from flask import jsonify, request, Response

FACEBOOK_VERIFY_TOKEN = "Shivansh"
FACEBOOK_PAGE_ACCESS_TOKEN = "EAAM3vu6VfC4BAMhnoJvCtSpQxCcBJBzMeBTbJL9crcm9fVdNp6lxPrZC153KbDPHl3ZCQWMSYU6lQbx5C2dByqhFzPw4z0fH4sJAjLF3YqZBlbkALfTT4UFE3F5OZBUOZCyTdZAGGc6W6BQoUwI9fyC9sk8TeYXZCnwBpoHeZCsL7DK8AlJ3MBTL"
FACEBOOK_SEND_URL = "https://graph.facebook.com/v2.6/me/messages?access_token=" + FACEBOOK_PAGE_ACCESS_TOKEN

@app.route("/")
def index():
	return "Hello World"

@app.route("/webhook", methods = ['GET', 'POST'])
def webhook():
	if request.method == "GET":
		verify_token = request.args.get('hub.verify_token')
		challenge = request.args.get('hub.challenge')
		if verify_token == FACEBOOK_VERIFY_TOKEN:
			return challenge
		else:
			return "Error"
	else:
		data = request.json
		print(data)
		if data["object"] == "page":
			for entry in data["entry"]:
				for messaging_event in entry["messaging"]:
					if messaging_event.get("message"):  
						msg = data['entry'][0]['messaging'][0]['message']['text']
						entities = data['entry'][0]['messaging'][0]['message']['nlp']['entities']
						sid = data['entry'][0]['messaging'][0]['sender']['id']
						requests.post(FACEBOOK_SEND_URL, headers = { "Content-Type": "application/json" }, data = send_message(sid, reply(msg, entities)))
		return "Ok"

def send_message(sid, msg):
	data = {
				"messaging_type": "RESPONSE",
				"recipient":
				{
					"id": sid
				},
				"message":
				{
					"text": msg
				}
			}
	return json.dumps(data)

def reply(msg, entities):
	nlp = dict()
	for i in entities.keys():
		nlp[i] = entities[i][0]['confidence']
	if max(nlp) == "greetings":
		return "Hello"
	elif max(nlp) == "thanks":
		return "You're welcome!"
	elif max(nlp) == "bye":
		return "See you"
	else:
		return max(nlp)
	
