from flask import Blueprint, redirect, url_for, request, jsonify
import requests
import json

from .extensions import db
from .models import Event

main = Blueprint('main', __name__)

@main.route('/events', methods=['POST'])
def insert_event():
    data = request.get_json()
    for event_data in data:
        event = Event(type=event_data['type'], date=event_data['date'])
        db.session.add(event)
    db.session.commit()
    return '', 200

@main.route('/events', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    return jsonify([{'type': event.type, 'date': event.date} for event in events])

@main.route('/events', methods=['DELETE'])
def clear_all_events():
    Event.query.delete()
    db.session.commit()
    return '', 200

@main.route('/control_message', methods=['GET'])
def get_control_message(self):
    # Send a GET request to the API
    response = requests.get(self.api_url + '/control_message', headers=self.headers, verify=True)

    # Check the response
    if response.status_code == 200:
        # Parse the control message from the response
        control_message = json.loads(response.text)['control_message']

        # Process the control message
        self.process_control_message(control_message)

        # Post the control message to the device
        self.post_control_message(control_message)
    else:
        print('Failed to get control message:', response.text)