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
		try:
			data = request.json
			print(data)
			if data["object"] == "page":
				for entry in data["entry"]:
					for messaging_event in entry["messaging"]:
						if messaging_event.get("message"):  
							if 'is_echo' in messaging_event['message'].keys():
								return "Ok"
							msg = messaging_event['message']['text']
							sid = messaging_event['sender']['id']
							rid = messaging_event['recipient']['id']
							if messaging_event['message'].get('nlp'):
								entities = data['entry'][0]['messaging'][0]['message']['nlp']['entities']
							else:
								entities = {}
							requests.post(FACEBOOK_SEND_URL, headers = { "Content-Type": "application/json" }, data = reply(msg, entities, sid))
			return "Ok"
		except:
			data = {
				"messaging_type": "RESPONSE",
				"recipient":
				{
					"id": "1899726730051482"
				},
				"message":
				{
					"text": "Error"
				}
			}
			data = json.dumps(data)
			requests.post(FACEBOOK_SEND_URL, headers = { "Content-Type": "application/json" }, data = data)


def reply(msg, entities, sid):
	name = get_user_data(sid)
	if not entities:
		return send_image(sid, msg)
	nlp = dict()
	for i in entities.keys():
		nlp[i] = entities[i][0]['confidence']
	if max(nlp) == "greetings":
		return send_message(sid, "Hello " + name)
	elif max(nlp) == "thanks":
		return send_message(sid, "You're welcome!")
	elif max(nlp) == "bye":
		return send_message(sid, "See you")
	else:
		return send_message(sid, max(nlp))

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

def send_image(sid, search):
	img_url = get_image(search)
	if img_url == "Not Found":
		return json.dumps({
				"messaging_type": "RESPONSE",
				"recipient":
				{
					"id": sid
				},
				"message":
				{
					"text": "No memes for " + search
				}
			})
	if img_url == "Error":
		return json.dumps({
				"messaging_type": "RESPONSE",
				"recipient":
				{
					"id": sid
				},
				"message":
				{
					"text": "Error"
				}
			})
	data = {
			  "recipient":{
			    			"id":sid
						  },
			  "message":{
					       "attachment":{
			    							"type":"image", 
			    							"payload":{
			        									"url":img_url, 
								        				"is_reusable":"True"
			    						      		  }
			    				         }
						}
			}
	print(data)		
	return json.dumps(data)

def get_image(search):
	try:
		url = "https://api.imgur.com/3/gallery/search/?q='" + search +" memes'"
		res = requests.request(url = url, method = 'GET', headers = { "Authorization": "Client-ID e21842678284d02", "Content-Type": "application/json" })
		if 'error' in res.json()["data"]:
			return "Error"
		if 'images' not in res.json()["data"][0]:
			return "Not Found"
		return res.json()["data"][0]["images"][0]["link"]
	except:
		return "Error"

def get_user_data(rid):
	FACEBOOK_USER_PROFILE = "https://graph.facebook.com/v2.6/" + rid + "?access_token=" + FACEBOOK_PAGE_ACCESS_TOKEN
	res = requests.get(FACEBOOK_USER_PROFILE, headers = { "Content-Type": "application/json" })
	if 'first_name' in res.json():
		return res.json()['first_name']
	else:
		return ""
		
