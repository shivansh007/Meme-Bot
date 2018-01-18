from src import app
from flask import jsonify, request

FACEBOOK_VERIFY_TOKEN = "Shivansh"

@app.route("/")
def index():
    return "Hello World"

@app.route("/webhook")
def webhook():
	print(request.args.get('hub.challenge'))
	query = request.args.get('query')
	if query and query[0]['hub.verify_token'] == FACEBOOK_VERIFY_TOKEN:
		return query[0]['hub.challenge']
	else:
		return "Error"
# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
