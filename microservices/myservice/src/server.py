from src import app
from flask import jsonify, request

FACEBOOK_VERIFY_TOKEN = "Shivansh"

@app.route("/")
def index():
    return "Hello World"

@app.route("/webhook")
def webhook():
	if request.query['hub.verify_token'] == FACEBOOK_VERIFY_TOKEN:
		return request.query['hub.challenge']
	else:
		return "Error"
# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
