from .extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)