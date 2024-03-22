from .extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)

class Control(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_status = db.Column(db.String(50), nullable=False)
    radar_status = db.Column(db.String(50), nullable=False)
    mute_status = db.Column(db.String(50), nullable=False)
    arm_status = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)