from src import app
from flask import jsonify, request

FACEBOOK_VERIFY_TOKEN = "Shivansh"
FACEBOOK_PAGE_ACCESS_TOKEN = "EAAM3vu6VfC4BAMhnoJvCtSpQxCcBJBzMeBTbJL9crcm9fVdNp6lxPrZC153KbDPHl3ZCQWMSYU6lQbx5C2dByqhFzPw4z0fH4sJAjLF3YqZBlbkALfTT4UFE3F5OZBUOZCyTdZAGGc6W6BQoUwI9fyC9sk8TeYXZCnwBpoHeZCsL7DK8AlJ3MBTL"

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
		print((request.json['entry'][0]['message']['text']))
		return jsonify(request.json)

# @app.route("/webhook", methods = ['POST'])
# def message():
# 	return request.args 
# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
