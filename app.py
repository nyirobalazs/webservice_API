from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)

@app.route('/events', methods=['POST'])
def insert_event():
    data = request.get_json()
    for event_data in data:
        event = Event(type=event_data['type'], date=event_data['date'])
        db.session.add(event)
    db.session.commit()
    return '', 200

@app.route('/control_message', methods=['GET'])
def get_control_message():
    # This is a placeholder. Replace this with the actual logic for retrieving the control message.
    return jsonify({'control_message': 'sync'})