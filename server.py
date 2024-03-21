from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, NoResultFound
from os import getenv

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'date': self.date
        }

class FallAPI:
    def __init__(self):
        self.app = Flask(__name__)
        # API_ADDRESS = 'postgresql://fallsensor_db_user:h3HKNB4YH19QpxuYRWPJxZF9oQHboILw@dpg-cnssqqla73kc73b6qefg-a.frankfurt-postgres.render.com/fallsensor_db'
        API_ADDRESS = getenv('DATABASE_URL')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = API_ADDRESS
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()  # Create all tables

        self.app.route('/events', methods=['POST'])(self.insert_event)
        self.app.route('/events', methods=['GET'])(self.get_events)
        self.app.route('/clear', methods=['DELETE'])(self.clear_events)

    def insert_event(self):
        try:
            data = request.get_json()
            for event_data in data:
                event = Event(type=event_data['type'], date=event_data['date'])
                db.session.add(event)
            db.session.commit()
            return '', 200
        except KeyError:
            return jsonify({'error': 'Invalid event data'}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Database error'}), 500

    def get_events(self):
        try:
            events = Event.query.all()
            return jsonify([event.serialize() for event in events]), 200
        except NoResultFound:
            return jsonify({'error': 'No events found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def clear_events(self):
        try:
            num_rows_deleted = db.session.query(Event).delete()
            db.session.commit()
            return jsonify({'message': f'{num_rows_deleted} rows deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
