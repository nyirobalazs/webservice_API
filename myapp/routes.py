from flask import Blueprint, redirect, url_for, request, jsonify

from .extensions import db
from .models import Event

main = Blueprint('main', __name__)

@app.route('/events', methods=['POST'])
def insert_event():
    data = request.get_json()
    for event_data in data:
        event = Event(type=event_data['type'], date=event_data['date'])
        db.session.add(event)
    db.session.commit()
    return '', 200

@app.route('/events', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    return jsonify([{'type': event.type, 'date': event.date} for event in events])

@app.route('/events', methods=['DELETE'])
def clear_all_events():
    Event.query.delete()
    db.session.commit()
    return '', 200

@app.route('/control_message', methods=['GET'])
def get_control_message():
    # This is a placeholder. Replace this with the actual logic for retrieving the control message.
    return jsonify({'control_message': 'sync'})
