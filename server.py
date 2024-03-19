from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    date = db.Column(db.DateTime)

@app.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    event = Event(type=data['type'], date=data['date'])
    db.session.add(event)
    db.session.commit()
    return {'id': event.id}, 201
