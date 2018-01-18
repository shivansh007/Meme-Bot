from src import app
from flask import jsonify, request

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
		res = request.json
		msg = res['entry'][0]['messaging'][0]['message']['text']
		sid = res['entry'][0]['messaging'][0]['sender']['id']
		return sendMsg(sid, msg)

def sendMsg(senderId, msg):
	return request(url = FACEBOOK_SEND_URL, method = 'POST', json = jsonify(messaging_type = "RESPONSE", recipient = jsonify(id = senderId), message = jsonify(text = msg)))