from flask import Blueprint, redirect, url_for, request, jsonify
import requests
import json

from .extensions import db
from .models import Event, Control

main = Blueprint('main', __name__)

@main.route('/add_events', methods=['POST'])
def insert_event():
    data = request.get_json()
    for event_data in data:
        event = Event(type=event_data['type'], date=event_data['date'])
        db.session.add(event)
    db.session.commit()
    print('Events added:', data)
    return '', 200

@main.route('/events', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    print('Events retrieved:', events)
    return jsonify([{'type': event.type, 'date': event.date} for event in events])

@main.route('/events', methods=['DELETE'])
def clear_all_events():
    Event.query.delete()
    db.session.commit()
    print('Events deleted')
    return '', 200

@main.route('/update_control', methods=['POST'])
def update_control():
    # Extract the control message from the request data
    control_message = request.get_json()

    # Update the database with the control message
    control = Control(camera_status=control_message['camera_status'],
                  radar_status=control_message['radar_status'],
                  mute_status=control_message['mute_status'],
                  arm_status=control_message['arm_status'],
                  date=control_message['date'])
    db.session.add(control)
    db.session.commit()

    print('Control message updated:', control_message)
    return '', 200

@main.route('/get_control', methods=['GET'])
def get_control():
    # Fetch the most recent control message from the database
    event = Event.query.order_by(Event.date.desc()).first()

    if event is not None:
        control_message = {
            'camera_status': event.camera_status,
            'radar_status': event.radar_status,
            'mute_status': event.mute_status,
            'arm_status': event.arm_status,
            'date': event.date
        }
        print('Control message:', control_message)
        return jsonify(control_message), 200
    else:
        print('No control message found')
        return '', 404

