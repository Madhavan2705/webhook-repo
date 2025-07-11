from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/github_webhooks?retryWrites=true&w=majority")
db = client.github_webhooks
events_collection = db.events

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return "No data received", 400

    action_type = None
    author = None
    from_branch = None
    to_branch = None
    timestamp = datetime.now(pytz.UTC).isoformat()

    if 'pusher' in data:
        action_type = 'push'
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]

    elif 'pull_request' in data:
        action_type = 'pull_request'
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']

    elif 'action' in data and data['action'] == 'closed' and 'pull_request' in data:
        if data['pull_request']['merged']:
            action_type = 'merge'
            author = data['pull_request']['user']['login']
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']

    else:
        return "Unhandled event", 200

    event = {
        "action_type": action_type,
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    }

    events_collection.insert_one(event)
    return jsonify({"status": "success"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(events_collection.find().sort("timestamp", -1).limit(10))
    for e in events:
        e['_id'] = str(e['_id'])
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
